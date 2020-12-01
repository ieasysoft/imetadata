# -*- coding: utf-8 -*- 
# @Time : 2020/9/11 15:57 
# @Author : 王西亚 
# @File : job_dm_path_parser.py

from __future__ import absolute_import

from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFileInfo import CDMFileInfo
from imetadata.business.metadata.base.fileinfo.c_dmPathInfo import CDMPathInfo
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_path_parser(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanfileprocessid = '{0}', dsdscanfilestatus = 2
where dsdid = (
  select dsdid  
  from   dm2_storage_directory 
  where  dsdscanfilestatus = 1 
    and dsdscanstatus = 0  
    and dsd_directory_valid = -1
    and dsddirtype <> '2'
  order by dsddirscanpriority desc, dsdaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage_directory.dsdid as query_dir_id
  , dm2_storage_directory.dsddirtype as query_dir_type
  , dm2_storage_directory.dsddirscanpriority as query_dir_scan_priority
  , dm2_storage_directory.dsdscanrule as query_dir_scanrule
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dsttype as query_storage_type
  , dm2_storage.dstOtherOption as query_storage_OtherOption  
  , COALESCE(dm2_storage_directory.dsd_object_id, dm2_storage_directory.dsdparentobjid)  as query_dir_parent_objid
  , dm2_storage_object.dsoobjecttype as query_dir_parent_objtype
from dm2_storage_directory 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  left join dm2_storage_object on dm2_storage_object.dsoid = COALESCE(dm2_storage_directory.dsd_object_id, dm2_storage_directory.dsdparentobjid) 
where dm2_storage_directory.dsdscanfileprocessid = '{0}'
            '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanfilestatus = 1, dsdscanfileprocessid = null 
where dsdscanfilestatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_id = dataset.value_by_name(0, 'query_dir_id', '')
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_storage_type = dataset.value_by_name(0, 'query_storage_type', self.Storage_Type_Core)

        # 将所有子目录, 文件的可用性, 都改为未知
        self.init_file_or_subpath_valid_unknown(ds_id)
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
        ds_root_path = dataset.value_by_name(0, 'query_rootpath', '')

        sql_get_rule = '''
        select dsdScanRule
        from dm2_storage_directory
        where dsdStorageid = :dsdStorageID and Position(dsddirectory || '{0}' in :dsdDirectory) = 1
            and dsdScanRule is not null
        order by dsddirectory desc
        limit 1
        '''.format(CFile.sep())
        rule_ds = CFactory().give_me_db(self.get_mission_db_id()).one_row(
            sql_get_rule,
            {
                'dsdStorageID': ds_storage_id,
                'dsdDirectory': ds_subpath
            }
        )
        ds_rule_content = rule_ds.value_by_name(0, 'dsScanRule', '')

        if ds_subpath == '':
            ds_subpath = ds_root_path
        else:
            ds_subpath = CFile.join_file(ds_root_path, ds_subpath)

        check_inbound_subpath_ready_flag_file = CUtils.equal_ignore_case(
            settings.application.xpath_one(
                self.path_switch(
                    self.Path_Setting_MetaData_InBound_Switch,
                    self.Switch_Use_Ready_Flag_File_Name
                ),
                self.Name_OFF
            ),
            self.Name_ON
        )
        inbound_subpath = CUtils.equal_ignore_case(
            ds_storage_type,
            self.Storage_Type_InBound) and CUtils.equal_ignore_case(ds_id,
                                                                    ds_storage_id)

        CLogger().debug('处理的目录为: {0}'.format(ds_subpath))
        try:
            self.parser_file_or_subpath_of_path(
                dataset, ds_id, ds_subpath, ds_rule_content,
                check_inbound_subpath_ready_flag_file,
                inbound_subpath
            )
            return CResult.merge_result(self.Success, '目录为[{0}]下的文件和子目录扫描处理成功!'.format(ds_subpath))
        except Exception as err:
            return CResult.merge_result(self.Failure, '目录为[{0}]下的文件和子目录扫描处理出现错误!错误原因为: {1}'.format(ds_subpath), err.__str__())
        finally:
            self.exchange_file_or_subpath_valid_unknown2invalid(ds_id)

    # check_inbound_subpath_ready_flag_file,
    # inbound_subpath
    def parser_file_or_subpath_of_path(self, dataset, ds_id, ds_path, ds_rule_content,
                                       check_inbound_subpath_ready_flag_file, inbound_subpath):
        """
        处理目录(完整路径)下的子目录和文件
        :param inbound_subpath:
        :param check_inbound_subpath_ready_flag_file: 是否检查入库子目录
        :param ds_rule_content:
        :param dataset: 数据集
        :param ds_id: 路径标识
        :param ds_path: 路径全名
        :return:
        """
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ignore_file_array = settings.application.xpath_one(self.Path_Setting_MetaData_InBound_ignore_file, None)
        ignore_dir_array = settings.application.xpath_one(self.Path_Setting_MetaData_InBound_ignore_dir, None)

        file_list = CFile.file_or_subpath_of_path(ds_path)
        for file_name in file_list:
            file_name_with_full_path = CFile.join_file(ds_path, file_name)

            if CFile.is_dir(file_name_with_full_path):
                CLogger().debug('在目录{0}下发现子目录: {1}'.format(ds_path, file_name))

                if CUtils.list_count(ignore_dir_array, file_name) > 0:
                    CLogger().debug('子目录: {0}在指定的忽略入库名单中, 将不入库! '.format(file_name))
                    continue

                path_shoule_inbound = True
                if path_shoule_inbound:
                    if check_inbound_subpath_ready_flag_file:
                        path_shoule_inbound = self.check_inbound_subpath_ready(file_name_with_full_path)

                if path_shoule_inbound:
                    path_obj = CDMPathInfo(
                        self.FileType_Dir,
                        file_name_with_full_path,
                        dataset.value_by_name(0, 'query_storage_id', ''),
                        None,
                        ds_id,
                        dataset.value_by_name(0, 'query_dir_parent_objid', None),
                        self.get_mission_db_id(),
                        ds_rule_content
                    )
                    if inbound_subpath:
                        # 注册到待入库请单中
                        self.register_2_inbound_list(
                            ds_storage_id,
                            path_obj.my_id,
                            CFile.file_relation_path(file_name_with_full_path, ds_path)
                        )

                    if path_obj.white_black_valid():
                        path_obj.db_check_and_update()
                    else:
                        CLogger().info('目录[{0}]未通过黑白名单检验, 不允许入库! '.format(file_name_with_full_path))
            elif CFile.is_file(file_name_with_full_path):
                if CUtils.list_count(ignore_file_array, file_name) > 0:
                    CLogger().debug('子目录: {0}在指定的忽略入库名单中, 将不入库! '.format(file_name))
                    continue

                CLogger().debug('在目录{0}下发现文件: {1}'.format(ds_path, file_name))
                file_obj = CDMFileInfo(
                    self.FileType_File, file_name_with_full_path,
                    dataset.value_by_name(0, 'query_storage_id', ''),
                    None,
                    ds_id,
                    dataset.value_by_name(0, 'query_dir_parent_objid', None),
                    self.get_mission_db_id(),
                    ds_rule_content
                )
                if file_obj.white_black_valid():
                    file_obj.db_check_and_update()
                else:
                    CLogger().info('文件[{0}]未通过黑白名单检验, 不允许入库! '.format(file_name_with_full_path))

        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage_directory
            set dsdscandirstatus = 0, dsdscanfilestatus = 0, dsddirscanpriority = 0
            where dsdid = :dsdid
            ''', {'dsdid': ds_id}
        )
        return CResult.merge_result(self.Success, '目录为[{0}]下的文件和子目录扫描处理成功!'.format(ds_path))

    def init_file_or_subpath_valid_unknown(self, ds_id):
        """
        将指定目录标识下的子目录和文件都更新为未知
        :param ds_id:
        :return:
        """
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_directory
            set dsd_directory_valid = {0}
            where dsdparentid = :id
            '''.format(self.File_Status_Unknown), {'id': ds_id})
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_file
            set dsffilevalid = {0}
            where dsfdirectoryid = :id
            '''.format(self.File_Status_Unknown), {'id': ds_id})

    def exchange_file_or_subpath_valid_unknown2invalid(self, ds_id):
        """
        将指定目录标识下的子目录和文件中, 可用性为未知的, 都更新为不可用
        :param ds_id:
        :return:
        """
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
                    update dm2_storage_directory
                    set dsd_directory_valid = {0}
                    where dsdparentid = :id and dsd_directory_valid = {1}
                    '''.format(self.File_Status_Invalid, self.File_Status_Unknown), {'id': ds_id})
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
                    update dm2_storage_file
                    set dsffilevalid = {0}
                    where dsfdirectoryid = :id and dsffilevalid = {1}
                    '''.format(self.File_Status_Invalid, self.File_Status_Unknown), {'id': ds_id})

    def check_inbound_subpath_ready(self, inbound_path) -> bool:
        inbound_ready_flag_filename_with_path = CFile.join_file(inbound_path, self.FileName_Ready_21AT)

        if CFile.file_or_path_exist(inbound_ready_flag_filename_with_path):
            return True
        else:
            CLogger().debug(
                '子目录[{0}]下没有找到入库标识文件[{1}], 表明数据还没有准备好, 暂不入库! '.format(inbound_path, self.FileName_Ready_21AT))
            return False

    def register_2_inbound_list(self, storage_id: str, directory_id: str, directory: str):
        database = CFactory().give_me_db(self.get_mission_db_id())
        new_batch_no = database.seq_next_value(self.Seq_Type_Date_AutoInc)
        sql_register_2_inbound_list = '''
        insert into dm2_storage_inbound(dsiid, dsistorageid, dsidirectory, dsibatchno, dsistatus, dsidirectoryid) 
        VALUES(:dsiid, :storageid, :directory, :batch_no, :status, :directory_id) 
        '''
        database.execute(
            sql_register_2_inbound_list,
            {
                'dsiid': CUtils.one_id(),
                'storageid': storage_id,
                'directory': directory,
                'batch_no': new_batch_no,
                'directory_id': directory_id,
                'status': self.ProcStatus_WaitConfirm
            }
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path_parser('', '').execute()
