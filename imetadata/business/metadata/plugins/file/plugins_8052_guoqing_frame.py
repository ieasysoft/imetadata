# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:27
# @Author : 赵宇飞
# @File : plugins_8052_guoqing_frame.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing


class plugins_8052_guoqing_frame(CFilePlugins_GUOTU_GuoQing):
    """
    与国情影像-整景纠正有差别(业务元数据xml的字段),xml文件的识别也不同，也不是***_21at.xml模式，所以直接继承于CFilePlugins_GUOTU
        数据内容	    文件格式	是否有坐标系	内容样例	说明
        影像文件	    tif/TIF	有	H50E003006AP005P2011A.TIF	融合影像文件
        元数据文件	xml/XML	无	H50E003006AP005P2011M.XML	整体元数据文件
    """
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-分幅影像'
        information[self.Plugins_Info_Name] = 'guoqing_frame'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_frame的验证规则（国情影像—分幅影像）
        todo 负责人 王学谦 在这里检验guoqing_frame的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__  # 初始化需要的参数
        file_path = self.file_info.__file_path__
        file_object_name = file_main_name[:]

        if len(file_main_name) >= 21:
            file_object_name = file_main_name[:20]  # 截取前20位
        elif len(file_main_name) == 20:  # 20位基本为附属文件
            pass
        else:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        file_main_name_with_path = CFile.join_file(file_path, file_object_name)
        check_file_main_name_exist = \
            CFile.file_or_path_exist('{0}o.{1}'.format(file_main_name_with_path, 'tif')) or \
            CFile.file_or_path_exist('{0}a.{1}'.format(file_main_name_with_path, 'tif'))
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self.__object_name__

        '''
        文件名第1，4，11，12，16，21位为字母，第2，3，5-10，14，15，17-20位是数字
        '''
        name_sub_1 = file_main_name[0:1]
        name_sub_2_to_3 = file_main_name[1:3]
        name_sub_4 = file_main_name[3:4]
        name_sub_5_to_10 = file_main_name[4:10]
        name_sub_11_to_12 = file_main_name[10:12]
        name_sub_14_to_15 = file_main_name[13:15]
        name_sub_16 = file_main_name[15:16]
        name_sub_17_to_20 = file_main_name[16:20]
        if CUtils.text_is_alpha(name_sub_1) is False \
                or CUtils.text_is_numeric(name_sub_2_to_3) is False \
                or CUtils.text_is_alpha(name_sub_4) is False \
                or CUtils.text_is_numeric(name_sub_5_to_10) is False \
                or CUtils.text_is_alpha(name_sub_11_to_12) is False \
                or CUtils.text_is_numeric(name_sub_14_to_15) is False \
                or CUtils.text_is_alpha(name_sub_16) is False \
                or CUtils.text_is_numeric(name_sub_17_to_20) is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        if len(file_main_name) == 21:
            name_sub_21 = file_main_name[20:21]
            if (CUtils.equal_ignore_case(name_sub_21.lower(), 'a')
                or CUtils.equal_ignore_case(name_sub_21.lower(), 'o')) \
                    and CUtils.equal_ignore_case(file_ext, 'tif'):
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = file_main_name
            else:
                self.__object_confirm__ = self.Object_Confirm_IKnown_Not
                self.__object_name__ = None
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        todo 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.__file_path__, self.file_info.__file_main_name__)
        metadata_main_name_with_path = metadata_main_name_with_path[:-1]
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file_Y = f'{metadata_main_name_with_path}Y.xml'
        temp_metadata_bus_file_M = f'{metadata_main_name_with_path}M.xml'
        temp_metadata_bus_file_P = f'{metadata_main_name_with_path}P.xml'
        if CFile.file_or_path_exist(temp_metadata_bus_file_Y):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_Y
        elif CFile.file_or_path_exist(temp_metadata_bus_file_M):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_M
        elif CFile.file_or_path_exist(temp_metadata_bus_file_P):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_P

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