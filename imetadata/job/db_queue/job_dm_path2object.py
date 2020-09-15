# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:31 
# @Author : 王西亚 
# @File : job_dm_path2object.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_xml import CXml
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.database.c_factory import CFactory
from imetadata.base.c_logger import CLogger
from imetadata.job.db_queue.c_dmBaseJob import CDMBaseJob


class job_dm_path2object(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdprocessid = '{0}', dsdscanstatus = 2
where dsdid = (
  select dsdid  
  from   dm2_storage_directory 
  where  dsdscanstatus = 1 and dsddirtype <> '2'
  order by dsdaddtime 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage.dstunipath as query_rootpath
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage.dstunipath || dm2_storage_directory.dsdpath as query_dir_full_path
  , dm2_storage_directory.dsddirectoryname as query_subpath_name
  , dm2_storage_directory.dsdid as query_dir_id
  , dm2_storage_directory.dsddirtype as query_dir_type
  , dm2_storage_directory.dsddirlastmodifytime as query_dir_lastmodifytime
  , dm2_storage.dstid as query_storage_id
  , dm2_storage_directory.dsd_object_type as query_dir_object_type
  , dm2_storage_directory.dsd_object_confirm as query_dir_object_confirm
  , dm2_storage_directory.dsd_object_id as query_dir_object_id
  , dm2_storage_directory.dsdscandirstatus as query_dir_ScanDirStatus
  , dm2_storage_directory.dsdparentobjid as query_dir_parent_objid
  , dm2_storage_object.dsoobjecttype as query_dir_parent_objtype
from dm2_storage_directory 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  left join dm2_storage_object on dm2_storage_object.dsoid = dm2_storage_directory.dsdparentobjid
where dm2_storage_directory.dsdprocessid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanstatus = 1, dsdprocessid = null 
where dsdscanstatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')

        if ds_subpath == '':
            ds_subpath = dataset.value_by_name(0, 'query_rootpath', '')
        else:
            ds_subpath = CFile.join_file(dataset.value_by_name(0, 'query_rootpath', ''), ds_subpath)
        CLogger().debug('处理的子目录为: {0}'.format(ds_subpath))

        if not CFile.file_or_path_exist(ds_subpath):
            self.bus_path_invalid(dataset, ds_subpath)
            return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_subpath))
        else:
            self.bus_path_valid(dataset, ds_subpath)

    def bus_path_invalid(self, dataset, path_name_with_full_path):
        """
        处理目录不存在时的业务
        :param dataset:
        :param path_name_with_full_path:
        :return:
        """
        path_name_with_relation_path = dataset.value_by_name(0, 'query_subpath', '')
        path_name_with_relation_path = CFile.join_file(path_name_with_relation_path, '')

        params = dict()
        params['dsdStorageID'] = dataset.value_by_name(0, 'query_storage_id', '')
        params['dsdSubDirectory'] = path_name_with_relation_path

        sql_update_file_invalid = '''
        update dm2_storage_file
        set dsffilevalid = 0, dsfscanstatus = 0
        where dsfdirectoryid in (
            select dsdid
            from dm2_storage_directory
            where dsdstorageid = '1'
              and dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
        )
        '''

        sql_update_path_invalid = '''
update dm2_storage_directory
set dsd_directory_valid = 0, dsdscanstatus = 0, dsdscanfilestatus = 0, dsdscandirstatus = 0
where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
        '''

        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_file_invalid, params)
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_path_invalid, params)

    def bus_path_valid(self, dataset, path_name_with_full_path):
        """
        处理目录存在时的业务:
        1. 检查目录下是否有metadata.rule
        :param dataset:
        :param path_name_with_full_path:
        :return:
        """

        params = dict()
        params['dsdID'] = dataset.value_by_name(0, 'query_dir_id', '')
        if CFile.file_or_path_exist(CFile.join_file(path_name_with_full_path, 'metadata.rule')):
            try:
                params['dsdScanRule'] = CXml.file_2_str(CFile.join_file(path_name_with_full_path, self.FileName_MetaData_Rule))
            except:
                params['dsdScanRule'] = None

        sql_update_path_valid = '''
        update dm2_storage_directory
        set dsd_directory_valid = -1, dsdscanrule = :dsdScanRule
        where dsdid = :dsdID
        '''

        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_path_valid, params)


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path2object('', '').execute()
