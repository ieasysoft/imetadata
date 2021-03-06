# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:21
# @Author : 赵宇飞
# @File : plugins_8050_guoqing_scene_noblock.py
import re

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing


class plugins_8050_guoqing_scene_noblock(CFilePlugins_GUOTU_GuoQing):
    """
    数据内容	文件格式	是否有坐标系	内容样例	                说明
    影像文件
    （至少有一个img）	img/IMG	有	GF2398924020190510F.img	融合影像文件，xxxF-n、xxxM-n、xxxP-n为一组
                                GF2398924020190510M.img	多光谱影像文件
                                GF2398924020190510P.img	全色波段影像文件
    元数据文件	    xml/XML	无	GF2398924020190510M.XML	多光谱元数据文件
                                GF2398924020190510P.XML	全色元数据文件
                                GF2398924020190510Y.XML	整体元数据文件
    关于正则表达式     https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '国情影像_整景纠正'
        information[self.Plugins_Info_Type_Title] = information[self.Plugins_Info_Type]
        # information[self.Plugins_Info_Name] = 'guoqing_scene_noblock'
        information[self.Plugins_Info_Type_Code] = '02010302'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_guoqing_scene'
        return information

    def classified(self):
        """
        设计国土行业数据guoqing_scene_noblock的验证规则（国情影像—非分块）,不带数字
        完成 负责人 王学谦 在这里检验guoqing_scene_noblock的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_path = self.file_info.file_path
        file_object_name = file_main_name[:]  # 这里需要取得规则匹配用的‘对象名’，即去除尾部字母等字符的名

        # 正则表达式，(?i)代表大小写不敏感，^代表字符串开头，$代表字符串结尾
        # [a-z]指匹配所有小写字母，配合(?i)匹配所有字母，{2}代表前面的匹配模式匹配2次，即[a-z]{2}匹配两个字母
        # \d匹配数字，即[0-9]，即\d+匹配一个或多个非空字符，\d{4}匹配四个任意数字
        # [0123]一般指匹配一个括号中任意字符，即匹配0到3
        # \S用于匹配所有非空字符，+代表匹配前面字符的数量为至少一个，即\S+匹配一个或多个非空字符
        if len(file_main_name) < 13:
            return self.Object_Confirm_IUnKnown, self._object_name
        # 下面正则：开头两个字母，字母后任意数量字符,而后匹配8位时间，4位任意数字（年份），[01]\d为月份，[0123]\d日
        if CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                r'\d{4}[01]\d[0123]\d[a-z]$'):  # 结尾为单个字母的情况
            file_object_name = file_main_name[:-1]  # 这里需要取得规则匹配用的‘对象名’，即去除尾部字母
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'  # 带-的抛出
                                                  r'\d{4}[01]\d[0123]\d[a-z][-]\d+$'):
            return self.Object_Confirm_IUnKnown, self._object_name
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'  # 尾部没字母取原本主名
                                                  r'\d{4}[01]\d[0123]\d$'):
            pass
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                  r'\d{4}[01]\d[0123]\d\S+$'):  # 结尾为多个的字符情况
            file_object_name_list = re.findall(r'(?i)^([a-z]{2}\S+\d{4}[01]\d[0123]\d)\S+$',
                                               file_main_name)
            file_object_name = file_object_name_list[0]  # 剔除结尾多个字符

        match_str = '(?i)^' + file_object_name + r'[FMP].img$'  # 匹配主文件的规则，即对象名+F/M/P
        check_file_main_name_exist = CFile.find_file_or_subpath_of_path(file_path, match_str, CFile.MatchType_Regex)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        """文件名第1-2位为字母，最后1位是字母在F/P/M中，倒数2-9位是数字"""
        name_sub_1_to_2 = file_object_name[0:2]
        name_sub_backwards_9_to_2 = file_object_name[-8:]
        if CUtils.text_is_alpha(name_sub_1_to_2) is False \
                or CUtils.text_is_numeric(name_sub_backwards_9_to_2) is False:
            return self.Object_Confirm_IUnKnown, self._object_name

        # 作为对象的主文件存在优先级，F-M-P,比如需要F的文件不存在，M才能是主文件
        # 能跑到这里的文件已经可以认为不是主文件，就是附属文件
        match_str_f = '(?i)^' + file_object_name + r'[F].img$'
        match_str_fm = '(?i)^' + file_object_name + r'[FM].img$'
        name_sub_backwards_1 = file_main_name[-1:]
        if CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'f') \
                and CUtils.equal_ignore_case(file_ext.lower(), 'img'):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
            self.add_file_to_detail_list(file_object_name)
        elif CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'm') \
                and CUtils.equal_ignore_case(file_ext.lower(), 'img') \
                and not CFile.find_file_or_subpath_of_path(file_path, match_str_f, CFile.MatchType_Regex):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
            self.add_file_to_detail_list(file_object_name)
        elif CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'p') \
                and CUtils.equal_ignore_case(file_ext.lower(), 'img') \
                and not CFile.find_file_or_subpath_of_path(file_path, match_str_fm, CFile.MatchType_Regex):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
            self.add_file_to_detail_list(file_object_name)
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name

    def add_file_to_detail_list(self, match_name):
        """
        设定国土行业数据国情的附属文件的验证规则（镶嵌影像）
        完成 负责人 王学谦 在这里检验国情的附属文件
        :return:
        """
        file_main_name = self._object_name
        file_path = self.file_info.file_path
        # 正则匹配附属文件
        if not CUtils.equal_ignore_case(file_path, ''):
            match_str = '{0}*.*'.format(match_name)
            match_file_list = CFile.file_or_dir_fullname_of_path(file_path, False, match_str, CFile.MatchType_Common)

            match_str_main_name = r'(?i)^{0}[FMP]$'.format(match_name)  # 主附属
            ext_list = ['rar', 'zip', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'xml']
            for file_with_path in match_file_list:
                if CUtils.equal_ignore_case(CFile.file_main_name(file_with_path), file_main_name):  # 去除自身与同名文件
                    pass
                elif CUtils.text_match_re(CFile.file_main_name(file_with_path), match_str_main_name):
                    self.add_file_to_details(file_with_path)  # 将文件加入到附属文件列表中
                elif CFile.file_ext(file_with_path).lower() in ext_list:
                    self.add_file_to_details(file_with_path)
                else:
                    pass

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        metadata_main_name_with_path = metadata_main_name_with_path[:-1]  # 去除尾部的F/M/P
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file_Y = '{0}Y.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_P = '{0}P.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_M = '{0}M.xml'.format(metadata_main_name_with_path)
        if CFile.file_or_path_exist(temp_metadata_bus_file_Y):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_Y
        elif CFile.file_or_path_exist(temp_metadata_bus_file_P):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_P
        elif CFile.file_or_path_exist(temp_metadata_bus_file_M):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_M

        if not check_file_metadata_bus_exist:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: self.metadata_bus_src_filename_with_path,
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '业务元数据[{0}]存在'.format(self.metadata_bus_src_filename_with_path)
                }
            )
