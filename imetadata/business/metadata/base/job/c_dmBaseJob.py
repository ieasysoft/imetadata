# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 11:41 
# @Author : 王西亚 
# @File : c_dmBaseJob.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob


class CDMBaseJob(CDBQueueJob):
    Path_MD_Bus_Root = '/root'
    Path_MD_Bus_ProductType = '{0}/ProductType'.format(Path_MD_Bus_Root)

    def metadata_bus_2_params(self, metadata_xml: CXml, params: dict):
        metadata_list = metadata_xml.xpath('{0}/*'.format(self.Path_MD_Bus_Root))
        for metadata_item in metadata_list:
            metadata_item_name = CXml.get_element_name(metadata_item).lower().strip()
            metadata_item_value = CXml.get_element_text(metadata_item).lower().strip()
            params[metadata_item_name] = metadata_item_value

    def clear_anything_in_directory(self, ds_storage_id, ds_ib_directory_name):
        CFactory().give_me_db(self.get_mission_db_id()).execute_batch(
            [
                (
                    '''
                    delete from dm2_storage_obj_detail
                    where dodobjectid in (
                      select dsd_object_id
                      from dm2_storage_directory
                      where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_obj_detail
                    where dodobjectid in (
                      select dsf_object_id
                      from dm2_storage_file
                      where dsfstorageid = :StorageID and position(:SubDirectory in dsffilerelationname) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_object
                    where dsoid in (
                      select dsd_object_id
                      from dm2_storage_directory
                      where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_object
                    where dsoid in (
                      select dsf_object_id
                      from dm2_storage_file
                      where dsfstorageid = :StorageID and position(:SubDirectory in dsffilerelationname) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_file
                    where dsfstorageid = :StorageID and position(:SubDirectory in dsffilerelationname) = 1
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_directory
                    where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_directory
                    where dsdstorageid = :StorageID and dsddirectory = :SubDirectory
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': ds_ib_directory_name
                    }
                )
            ]
        )

    def get_object_info(self, object_id, object_data_type):
        sql_get_info = ''
        if CUtils.equal_ignore_case(object_data_type, self.FileType_Dir):
            sql_get_info = '''
            select 
                coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_directory.dsddirectory as query_object_fullname   
                , dm2_storage_directory.dsd_directory_valid as query_object_valid  
                , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_object_root_dir 
                , dm2_storage.dstid as query_object_storage_id
                , dm2_storage_directory.dsddirectory as query_object_relation_path
                , dm2_storage_directory.dsdid as query_object_file_id
                , dm2_storage_directory.dsdparentid as query_object_file_parent_id
                , dm2_storage_object.dsoparentobjid as query_object_owner_id
            from dm2_storage_object, dm2_storage_directory, dm2_storage  
            where 
                dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id    
                and dm2_storage_directory.dsdstorageid = dm2_storage.dstid    
                and dm2_storage_object.dsoid = :dsoid
            '''
            return CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_info, {'dsoid': object_id})
        elif CUtils.equal_ignore_case(object_data_type, self.FileType_File):
            sql_get_info = '''
            select 
                coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_file.dsffilerelationname as query_object_fullname 
                , dm2_storage_file.dsffilevalid as query_object_valid     
                , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_object_root_dir 
                , dm2_storage.dstid as query_object_storage_id
                , dm2_storage_file.dsffilerelationname as query_object_relation_path
                , dm2_storage_file.dsfid as query_object_file_id
                , dm2_storage_file.dsfdirectoryid as query_object_file_parent_id
                , dm2_storage_object.dsoparentobjid as query_object_owner_id
            from dm2_storage_object, dm2_storage_file, dm2_storage, dm2_storage_directory   
            where dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id 
                and dm2_storage_file.dsfstorageid = dm2_storage.dstid 
                and dm2_storage_directory.dsdid = dm2_storage_file.dsfdirectoryid 
                and dm2_storage_object.dsoid = :dsoid
            '''
            return CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_info, {'dsoid': object_id})
        else:
            sql_get_parent_object_id = '''
            select dm2_storage_object.dsoid, dm2_storage_object.dsoobjectname, dm2_storage_object.dsodatatype 
            from dm2_storage_object 
            where dsoid = (select dsoparentobjid from dm2_storage_object where dsoid = :object_id)
            '''
            ds_parent_object = CFactory().give_me_db(self.get_mission_db_id()).one_row(
                sql_get_parent_object_id,
                {'object_id': object_id}
            )
            if ds_parent_object.is_empty():
                raise Exception('找不到数据[{0}]的所属数据, 无法继续处理!'.format(object_id))

            return self.get_object_info(
                ds_parent_object.value_by_name(0, 'dsoid', '')
                , ds_parent_object.value_by_name(0, 'dsodatatype', '')
            )
