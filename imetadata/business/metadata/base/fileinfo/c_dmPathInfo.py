# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:45 
# @Author : 王西亚 
# @File : c_dmPathInfo.py
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.manager.c_pluginsMng import CPluginsMng
from imetadata.database.c_factory import CFactory


class CDMPathInfo(CDMFilePathInfoEx):
    def custom_init(self):
        """
        自定义初始化方法
        :return:
        """
        engine = CFactory().give_me_db(self.__db_server_id__)
        if self.__my_id__ is None:
            self.__ds_file_or_path__ = engine.one_row(
                'select dsdid, dsdparentid, dsddirectory, dsddirtype, dsddirectoryname, dsd_object_type, \
                        dsd_object_confirm, dsd_object_id, dsd_directory_valid, dsdpath, dsddircreatetime, \
                        dsddirlastmodifytime, dsdparentobjid, dsdscanrule from dm2_storage_directory \
                        where dsdstorageid = :dsdStorageID and dsddirectory = :dsdDirectory',
                {'dsdStorageID': self.__storage_id__, 'dsdDirectory': self.__file_name_with_rel_path__})
            if not self.__ds_file_or_path__.is_empty():
                self.__my_id__ = self.__ds_file_or_path__.value_by_name(0, 'dsdid', None)
            if self.__my_id__ is None:
                self.__my_id__ = CUtils.one_id()
        else:
            self.__ds_file_or_path__ = engine.one_row(
                'select dsdid, dsdparentid, dsddirectory, dsddirtype, dsddirectoryname, dsd_object_type, \
                        dsd_object_confirm, dsd_object_id, dsd_directory_valid, dsdpath, dsddircreatetime, \
                        dsddirlastmodifytime, dsdparentobjid, dsdscanrule from dm2_storage_directory \
                        where dsdid = :dsdID',
                {'dsdid': self.__my_id__})

    def db_update_status_on_path_invalid(self):
        """
        处理目录不存在时的业务
        1. 标记已经入库的文件为无效
        1. 标记已经入库的子目录为无效
        :return:
        """
        path_name_with_relation_path = CFile.join_file(self.__file_path_with_rel_path__, '')

        params = dict()
        params['dsdStorageID'] = self.__storage_id__
        params['dsdSubDirectory'] = path_name_with_relation_path

        sql_update_file_invalid = '''
            update dm2_storage_file
            set dsffilevalid = 0, dsfscanstatus = 0
            where dsfdirectoryid in (
                select dsdid
                from dm2_storage_directory
                where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
            )
            '''

        sql_update_path_invalid = '''
            update dm2_storage_directory
            set dsd_directory_valid = 0, dsdscanstatus = 0, dsdscanfilestatus = 0, dsdscandirstatus = 0
            where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
            '''

        engine = CFactory().give_me_db(self.__db_server_id__)
        session = engine.give_me_session()
        try:
            engine.session_execute(session, sql_update_file_invalid, params)
            engine.session_execute(session, sql_update_path_invalid, params)
            engine.session_commit(session)
        except Exception as error:
            CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__))
            engine.session_rollback(session)
        finally:
            engine.session_close(session)

    def db_path2object(self):
        """
        :return:
        """

        db_object_confirm = self.__ds_file_or_path__.value_by_name(0, 'dsd_object_confirm',
                                                                   self.Object_Confirm_IUnKnown)

        if (db_object_confirm == self.Object_Confirm_IKnown) or (db_object_confirm == self.Object_Confirm_Maybe):
            db_path_modify_time = self.__ds_file_or_path__.value_by_name(0, 'dsddirlastmodifytime', '')
            if CUtils.equal_ignore_case(CUtils.any_2_str(db_path_modify_time),
                                        CUtils.any_2_str(self.__file_modify_time__)):
                CLogger().info('目录[{0}]的最后修改时间, 和库中登记的没有变化, 对象识别将被忽略! '.format(self.__file_name_with_full_path__))
                return
            else:
                # 删除对象记录, 清理对象字段
                db_object_id = self.__ds_file_or_path__.value_by_name(0, 'dsd_object_id', '')
                db_object_type = self.__ds_file_or_path__.value_by_name(0, 'dsd_object_type', '')
                CLogger().debug(
                    '系统发现目录{0}的最后修改时间有变化, 将删除它关联的对象{1}.{2}, 重新识别'.format(self.__file_main_name__, db_object_type,
                                                                         db_object_id))
                self.db_delete_object_by_id(db_object_id)

        object_confirm = self.Object_Confirm_IUnKnown
        object_name = None
        object_type = None
        classified_obj = CPluginsMng.plugins_classified(self)
        if classified_obj is not None:
            object_confirm = classified_obj.classified_object_confirm
            object_name = classified_obj.classified_object_name
            object_type = classified_obj.get_id()

        if (object_confirm == self.Object_Confirm_IUnKnown) or (object_confirm == self.Object_Confirm_IKnown_Not):
            sql_update_path_object = '''
                update dm2_storage_directory
                set dsd_object_confirm = :dsd_object_confirm, dsd_object_id = null, dsd_object_type = null
                    , dsdscanfilestatus = 1, dsdscandirstatus = 1, dsd_directory_valid = -1, dsddirlastmodifytime = :fileModifyTime
                where dsdid = :dsdid
                '''
            CFactory().give_me_db(self.__db_server_id__).execute(sql_update_path_object, {'dsdid': self.__my_id__,
                                                                                          'dsd_object_confirm': object_confirm,
                                                                                          'fileModifyTime': CUtils.any_2_str(
                                                                                              self.__file_modify_time__)})
        else:
            sql_insert_object = '''
                insert into dm2_storage_object(dsoid, dsoobjectname, dsoobjecttype, dsodatatype, dsoalphacode, dsoaliasname, dsoparentobjid) 
                values(:dsoid, :dsoobjectname, :dsoobjecttype, :dsodatatype, :dsoalphacode, :dsoaliasname, :dsoparentobjid)
                '''

            new_dso_id = CUtils.one_id()

            sql_update_path_object = '''
                update dm2_storage_directory
                set dsd_object_confirm = :dsd_object_confirm, dsd_object_id = :dsd_object_id, dsd_object_type = :dsd_object_type
                    , dsdscanfilestatus = 0, dsdscandirstatus = 0, dsd_directory_valid = -1, dsddirlastmodifytime = :fileModifyTime
                where dsdid = :dsdid
                '''

            engine = CFactory().give_me_db(self.__db_server_id__)
            session = engine.give_me_session()
            try:
                params = dict()
                params['dsoid'] = new_dso_id
                params['dsoobjectname'] = object_name
                params['dsoobjecttype'] = object_type
                params['dsodatatype'] = self.FileType_Dir
                params['dsoalphacode'] = object_name
                params['dsoaliasname'] = object_name
                params['dsoparentobjid'] = self.__owner_obj_id__
                engine.session_execute(session, sql_insert_object, params)

                params = dict()
                params['dsdid'] = self.__my_id__
                params['dsd_object_confirm'] = object_confirm
                params['dsd_object_id'] = new_dso_id
                params['dsd_object_type'] = object_type
                params['fileModifyTime'] = CUtils.any_2_str(self.__file_modify_time__)
                engine.session_execute(session, sql_update_path_object, params)

                engine.session_commit(session)
            except Exception as error:
                CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__))
                engine.session_rollback(session)
            finally:
                engine.session_close(session)

    def db_check_and_update_metadata_rule(self, metadata_rule_file_name):
        """
        检查并判断指定的元数据扫描规则文件是否与数据库中的记录相等
        1. 如果和记录中的不同
            删除当前目录下的所有子目录, 文件 和对象
            更新记录中的规则
            设置子目录扫描状态为正常
        2. 如果和记录中的相同
            返回
        :param metadata_rule_file_name:
        :return:
        """
        metadata_rule_content = ''
        if CFile.file_or_path_exist(metadata_rule_file_name):
            try:
                metadata_rule_content = CXml.file_2_str(metadata_rule_file_name)
                CLogger().debug(
                    '在目录[{0}]下发现元数据规则文件, 它的内容为[{1}]'.format(self.__file_name_with_full_path__, metadata_rule_content))
            except:
                pass

        db_metadata_rule_content = self.__ds_file_or_path__.value_by_name(0, 'dsdscanrule', '')
        CLogger().debug(
            '目录[{0}]在库中登记的规则内容为[{1}]'.format(self.__file_name_with_full_path__, db_metadata_rule_content))

        if CUtils.equal_ignore_case(metadata_rule_content, db_metadata_rule_content):
            CLogger().debug(
                '目录[{0}]的规则内容与库中的相同'.format(self.__file_name_with_full_path__))
            return
        else:
            CLogger().debug(
                '目录[{0}]的规则内容与库中的不同, 将清理目录下的文件, 重新入库!'.format(self.__file_name_with_full_path__))

        sql_update_path_scan_rule = '''
            update dm2_storage_directory
            set dsd_directory_valid = -1, dsdscanrule = :dsdScanRule 
            where dsdid = :dsdID
            '''

        sql_clear_files_of_path = '''
            delete from dm2_storage_file
            where dsfdirectoryid in (
                select dsdid
                from dm2_storage_directory
                where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1 
            )
            '''
        sql_clear_subpath_of_path = '''
            delete from dm2_storage_directory
            where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1 
              and dsdid <> :dsdID
            '''

        engine = CFactory().give_me_db(self.__db_server_id__)
        session = engine.give_me_session()
        try:
            params = dict()
            params['dsdID'] = self.__my_id__
            if metadata_rule_content == '':
                params['dsdScanRule'] = None
            else:
                params['dsdScanRule'] = metadata_rule_content
            engine.session_execute(session, sql_update_path_scan_rule, params)

            params = dict()
            params['dsdID'] = self.__my_id__
            params['dsdStorageID'] = self.__storage_id__
            params['dsdSubDirectory'] = CFile.join_file(self.__file_name_with_rel_path__, '')

            engine.session_execute(session, sql_clear_files_of_path, params)
            engine.session_execute(session, sql_clear_subpath_of_path, params)

            engine.session_commit(session)
        except Exception as error:
            CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__))
            engine.session_rollback(session)
        finally:
            engine.session_close(session)

    def db_check_and_update(self):
        """
        检查并更新dm2_storage_directory表中记录
        :return:
        """
        if not self.__ds_file_or_path__.is_empty():
            # 如果记录已经存在
            db_path_modify_time = self.__ds_file_or_path__.value_by_name(0, 'dsddirlastmodifytime', '')
            if CUtils.equal_ignore_case(CUtils.any_2_str(db_path_modify_time),
                                        CUtils.any_2_str(self.__file_modify_time__)):
                CLogger().info('目录[{0}]的最后修改时间, 和库中登记的没有变化, 子目录将被设置为忽略刷新! '.format(self.__file_name_with_full_path__))
                CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_directory set dsdScanStatus = 0, dsdScanFileStatus = 0, dsd_directory_valid = -1
                    where dsdid = :dsdid 
                    ''', {'dsdid': self.__my_id__})
            else:
                CLogger().info('目录[{0}]的最后修改时间, 和库中登记的有变化, 子目录将被设置为重新刷新! '.format(self.__file_name_with_full_path__))
                CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_directory set dsdScanStatus = 1, dsdScanFileStatus = 1, dsd_directory_valid = -1
                    where dsdid = :dsdid 
                    ''', {'dsdid': self.__my_id__})
        else:
            CLogger().info('目录[{0}]未在库中登记, 系统将登记该记录! '.format(self.__file_name_with_full_path__))
            self.db_insert()

    def db_insert(self):
        """
        将当前目录, 创建一条新记录到dm2_storage_directory表中
        :return:
        """
        sql_insert = '''
        insert into dm2_storage_directory(dsdid, dsdparentid, dsdstorageid, dsddirectory, dsddirtype, dsdlastmodifytime, 
            dsddirectoryname, dsdpath, dsddircreatetime, dsddirlastmodifytime, dsdparentobjid, 
            dsdscanstatus, dsdscanfilestatus, dsdscandirstatus, dsd_directory_valid) 
        values(:dsdid, :dsdparentid, :dsdstorageid, :dsddirectory, :dsddirtype, now(), 
            :dsddirectoryname, :dsdpath, :dsddircreatetime, :dsddirlastmodifytime, :dsdparentobjid,
            1, 1, 1, -1)
        '''
        params = dict()
        params['dsdid'] = self.__my_id__
        params['dsdparentid'] = self.__parent_id__
        params['dsdstorageid'] = self.__storage_id__
        params['dsddirectory'] = self.__file_name_with_rel_path__
        params['dsddirtype'] = self.Dir_Type_Directory
        params['dsddirectoryname'] = self.__file_name_without_path__
        params['dsdpath'] = self.__file_path_with_rel_path__
        params['dsddircreatetime'] = self.__file_create_time__
        params['dsddirlastmodifytime'] = self.__file_modify_time__
        params['dsdparentobjid'] = self.__owner_obj_id__
        CFactory().give_me_db(self.__db_server_id__).execute(sql_insert, params)