# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_filePlugins_guotu.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class CDirPlugins_keyword(CDirPlugins):
    def get_information(self) -> dict:
        information = dict()
        information[self.Plugins_Info_ID] = self.get_id()
        information[self.Plugins_Info_Title] = information[self.Plugins_Info_ID]
        information[self.Plugins_Info_ViewEngine] = None
        information[self.Plugins_Info_SpatialEngine] = None
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_TagsEngine] = None
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_Module_Distribute_Engine] = None  # 同步的引擎，值是发布同步用的类的名字
        return information

    def classified(self):
        """
        关键字识别
        """
        super().classified()
        # 预获取需要的参数
        file_path = self.file_info.file_path
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext

        # 预定义逻辑参数 数据文件匹配
        object_file_name_flag = False
        object_file_path_flag = False
        object_file_ext_flag = False
        object_file_affiliated_flag = False
        object_keyword_list = self.get_classified_character_of_object_keyword()
        if len(object_keyword_list) > 0:
            for keyword_info in object_keyword_list:
                keyword_id = CUtils.dict_value_by_name(keyword_info, self.Name_ID, None)
                regex_match = CUtils.dict_value_by_name(keyword_info, self.TextMatchType_Regex, '.*')
                if CUtils.equal_ignore_case(keyword_id, self.Name_FileName):
                    if CUtils.text_match_re(file_main_name, regex_match):
                        object_file_name_flag = True
                elif CUtils.equal_ignore_case(keyword_id, self.Name_FilePath):
                    if CUtils.text_match_re(file_path, regex_match):
                        object_file_path_flag = True
                elif CUtils.equal_ignore_case(keyword_id, self.Name_FileExt):
                    if CUtils.text_match_re(file_ext, regex_match):
                        object_file_ext_flag = True
                elif CUtils.equal_ignore_case(keyword_id, self.Name_FileAffiliated):
                    affiliated_file_path = CUtils.dict_value_by_name(keyword_info, self.Name_FilePath, None)
                    if affiliated_file_path is not None:
                        if CFile.find_file_or_subpath_of_path(affiliated_file_path, regex_match,
                                                              CFile.MatchType_Regex):
                            object_file_affiliated_flag = True
                    else:
                        if CFile.find_file_or_subpath_of_path(file_path, regex_match,
                                                              CFile.MatchType_Regex):
                            object_file_affiliated_flag = True

        # 预定义逻辑参数 附属文件匹配
        affiliated_file_name_flag = False
        affiliated_file_path_flag = False
        affiliated_file_ext_flag = False
        affiliated_file_main_flag = False
        affiliated_keyword_list = self.get_classified_character_of_affiliated_keyword()
        if len(affiliated_keyword_list) > 0:
            for keyword_info in affiliated_keyword_list:
                keyword_id = CUtils.dict_value_by_name(keyword_info, self.Name_ID, None)
                regex_match = CUtils.dict_value_by_name(keyword_info, self.TextMatchType_Regex, '.*')
                if CUtils.equal_ignore_case(keyword_id, self.Name_FileName):
                    if CUtils.text_match_re(file_main_name, regex_match):
                        affiliated_file_name_flag = True
                elif CUtils.equal_ignore_case(keyword_id, self.Name_FilePath):
                    if CUtils.text_match_re(file_path, regex_match):
                        affiliated_file_path_flag = True
                elif CUtils.equal_ignore_case(keyword_id, self.Name_FileExt):
                    if CUtils.text_match_re(file_ext, regex_match):
                        affiliated_file_ext_flag = True
                elif CUtils.equal_ignore_case(keyword_id, self.Name_FileAffiliated):
                    affiliated_file_path = CUtils.dict_value_by_name(keyword_info, self.Name_FilePath, None)
                    if affiliated_file_path is not None:
                        if CFile.find_file_or_subpath_of_path(affiliated_file_path, regex_match,
                                                              CFile.MatchType_Regex):
                            affiliated_file_main_flag = True
                    else:
                        if CFile.find_file_or_subpath_of_path(file_path, regex_match,
                                                              CFile.MatchType_Regex):
                            affiliated_file_main_flag = True

        if object_file_name_flag and object_file_path_flag and \
                object_file_ext_flag and object_file_affiliated_flag:
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        elif affiliated_file_name_flag and affiliated_file_path_flag and \
                affiliated_file_ext_flag and affiliated_file_main_flag:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
        else:
            self._object_confirm = self.Object_Confirm_IUnKnown
            self._object_name = None

        return self._object_confirm, self._object_name

    @abstractmethod
    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.TextMatchType_Regex: None  # 配置数据文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,
                self.TextMatchType_Regex: None  # 配置数据文件路径的匹配规则
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.TextMatchType_Regex: None  # 配置数据文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileAffiliated,
                self.Name_FilePath: None,  # 配置需要验证附属文件存在性的 文件路径
                self.TextMatchType_Regex: None   # 配置需要验证附属文件的匹配规则,对于文件全名匹配
            }
        ]

    @abstractmethod
    def get_classified_character_of_affiliated_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.TextMatchType_Regex: None  # 配置附属文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,
                self.TextMatchType_Regex: None  # 配置附属文件路径的匹配规则
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.TextMatchType_Regex: None  # 配置附属文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileMain,
                self.Name_FilePath: None,  # 配置需要验证主文件存在性的 文件路径
                self.TextMatchType_Regex: None   # 配置需要验证主文件的匹配规则,对于文件全名匹配
            }
        ]