# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 11:53 
# @Author : 王西亚 
# @File : job_dm_obj_metadata.py


from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.manager.c_pluginsMng import CPluginsMng
from imetadata.database.c_factory import CFactory


class job_dm_obj_metadata(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsometadataparseprocid = '{0}', dsometadataparsestatus = 2
where dsoid = (
  select dsoid  
  from   dm2_storage_object 
  where  dsometadataparsestatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dsoid, dsodatatype, dsoobjecttype, dsoobjectname from dm2_storage_object where dsometadataparseprocid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsometadataparsestatus = 1, dsometadataparseprocid = null 
where dsometadataparsestatus = 2
        '''

    def process_mission(self, dataset):
        dso_id = dataset.value_by_name(0, 'dsoid', '')
        dso_data_type = dataset.value_by_name(0, 'dsodatatype', '')
        dso_object_type = dataset.value_by_name(0, 'dsoobjecttype', '')
        dso_object_name = dataset.value_by_name(0, 'dsoobjectname', '')

        CLogger().debug('开始处理对象: {0}.{1}.{2}.{3}的元数据'.format(dso_id, dso_data_type, dso_object_type, dso_object_name))

        ds_file_info = self.get_object_info(dso_id, dso_data_type)

        if ds_file_info.value_by_name(0, 'query_object_valid', self.DB_False) == self.DB_False:
            CFactory().give_me_db(self.get_mission_db_id()).execute('''
                update dm2_storage_object
                set dsometadataparsestatus = 0
                  , dsolastmodifytime = now()
                  , dsometadataparsememo = '文件或目录不存在，元数据无法解析'
                where dsoid = :dsoid
                ''', {'dsoid': dso_id})
            return CResult.merge_result(self.Success, '文件或目录[{0}]不存在，元数据无法解析, 元数据处理正常结束!'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', '')))

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
                'dsdStorageID': ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
                'dsdDirectory': ds_file_info.value_by_name(0, 'query_object_relation_path', '')
            }
        )
        ds_rule_content = rule_ds.value_by_name(0, 'dsScanRule', '')
        file_info_obj = CDMFilePathInfoEx(
            dso_data_type,
            ds_file_info.value_by_name(0, 'query_object_fullname', ''),
            ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
            ds_file_info.value_by_name(0, 'query_object_file_id', ''),
            ds_file_info.value_by_name(0, 'query_object_file_parent_id', ''),
            ds_file_info.value_by_name(0, 'query_object_owner_id', ''),
            self.get_mission_db_id(),
            ds_rule_content
        )
        plugins_obj = CPluginsMng.plugins(file_info_obj, dso_object_type)
        if plugins_obj is None:
            return CResult.merge_result(
                self.Failure,
                '文件或目录[{0}]的类型插件[{1}]不存在，元数据无法解析, 处理结束!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''),
                    dso_object_type
                )
            )

        plugins_obj.classified()
        if not plugins_obj.create_virtual_content():
            self.db_update_object_status(dso_id, '文件或目录[{0}]的内容解析失败, 元数据无法提取!'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', '')))
        try:
            metadata_parser = CMetaDataParser(
                dso_id, dso_object_name, file_info_obj, plugins_obj.file_content,
                plugins_obj.get_information()
            )
            process_result = plugins_obj.parser_metadata(metadata_parser)

            if CResult.result_success(process_result):
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dm2_storage_object
                    set dsometadataparsestatus = 0
                      , dsolastmodifytime = now()
                    where dsoid = :dsoid
                    ''',
                    {'dsoid': dso_id}
                )
                return CResult.merge_result(self.Success, '文件或目录[{0}]元数据解析成功结束!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', '')))
            else:
                self.db_update_object_status(dso_id, '文件或目录[{0}]元数据解析过程出现错误! 错误原因为: {1}'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''), CResult.result_message(process_result)))
                return process_result
        except Exception as error:
            self.db_update_object_status(dso_id, '文件或目录[{0}]元数据解析过程出现错误! 错误原因为: {1}'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', ''), error.__str__()))

            return CResult.merge_result(self.Failure, '文件或目录[{0}]元数据解析过程出现错误! 错误原因为: {1}'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', ''), error.__str__()))
        finally:
            plugins_obj.destroy_virtual_content()

    def db_update_object_status(self, dso_id, memo):
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_object
            set dsometadataparsestatus = 3
              , dsolastmodifytime = now()
              , dsometadataparsememo = :dsometadataparsememo
            where dsoid = :dsoid
            ''', {'dsoid': dso_id, 'dsometadataparsememo': memo})


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_obj_metadata('', '').execute()
