# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_wfv.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf1_pms_and_wfv import \
    CSatFilePlugins_gf1_pms_and_wfv


class CSatFilePlugins_gf1_wfv(CSatFilePlugins_gf1_pms_and_wfv):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF1_WFV'
        information[self.Plugins_Info_Type_Title] = '高分一号WFV传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式

        样例：GF1_WFV1_E73.2_N39.7_20131008_L1A0000095560.tiff
        """
        # 支持的类型有：DIR和ZIP GF1_WFV1_E65.2_N26.6_20130927_L1A0000090284
        #                    GF1_WFV2_E65.2_N26.6_20130927_L1A0000090284
        #            File    GF1_WFV1_E65.2_N26.6_20130927_L1A0000090284-PAN1.tiff
        #                    GF1_WFV2_E65.2_N26.6_20130927_L1A0000090284-PAN2.tiff
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^GF1_WFV.*[_].*', self.TextMatchType_Regex
        else:
            return r'(?i)^GF1_WFV.*[_].*[.]tiff$', self.TextMatchType_Regex

    def get_classified_object_name_of_sat(self, sat_file_status) -> str:
        """
        当卫星数据是解压后的散落文件时, 如何从解压后的文件名中, 解析出卫星数据的原名
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        . 如果是散落文件, 则是针对文件的全名
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        """
        if sat_file_status == self.Sat_Object_Status_Zip or sat_file_status == self.Sat_Object_Status_File:
            return self.file_info.file_main_name
        elif sat_file_status == self.Sat_Object_Status_Dir:
            return self.file_info.file_name_without_path

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 文件的质检列表
        质检项目应包括并不限于如下内容:
        1. 实体数据的附属文件是否完整, 实体数据是否可以正常打开和读取
        1. 元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        1. 业务元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        示例:
        return [
            {self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()), self.Name_ID: 'pan_tif',
             self.Name_Title: '全色文件', self.Name_Type: self.QualityAudit_Type_Error}
            , {self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()), self.Name_ID: 'mss_tif',
               self.Name_Title: '多光谱文件', self.Name_Type: self.QualityAudit_Type_Error}
        ]
        :param parser:
        :return:
        """
        return [
            {
                self.Name_FileName: '{0}.tiff'.format(self.classified_object_name()),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '影像文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_FileName: '{0}.xml'.format(self.classified_object_name()),
                self.Name_ID: 'bus_xml',
                self.Name_Title: '业务元数据',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def get_metadata_bus_configuration_list(self) -> list:
        """
        固定的列表，重写时不可缺项
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # 卫星，必填，从元数据组织定义，必须是标准命名的卫星名称
                self.Name_XPath: '/ProductMetaData/SatelliteID'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/ProductMetaData/SensorID'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_Value: None
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/ProductMetaData/TopLeftLatitude'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/ProductMetaData/TopLeftLongitude'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/ProductMetaData/TopRightLatitude'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/ProductMetaData/TopRightLongitude'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/ProductMetaData/BottomRightLatitude'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/ProductMetaData/BottomRightLongitude'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/ProductMetaData/BottomLeftLatitude'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/ProductMetaData/BottomLeftLongitude'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/ProductMetaData/CenterTime'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/ProductMetaData/ImageGSD',
                self.Name_Value: 2
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/ProductMetaData/RollViewingAngle'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/ProductMetaData/CloudPercent'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/ProductMetaData/OrbitID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/ProductMetaData/ProduceTime',
            },
            {
                self.Name_ID: 'remark',  # 备注 可空
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productname',  # 产品名称，有的能从卫星元数据里面取，没有就不取
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'producttype',  # 产品类型 必填
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_ProductType, None)
            },
            {
                self.Name_ID: 'productattribute',  # 产品属性 必填
                self.Name_XPath: '/ProductMetaData/ProductLevel',
                self.Name_Map: {  # 映射，当取到的值为key时，将值转换为value
                    'LEVEL1A': 'L1',
                    'LEVEL2A': 'L2',
                    'LEVEL4A': 'L4'
                    # self.Name_Default: None # 没有对应的的映射使用默认值
                }
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: '/ProductMetaData/ProductID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，放文件全路径即可
                self.Name_XPath: None,
                self.Name_Value: None
            }
        ]

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            '{0}.xml'.format(self.classified_object_name())
        )

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: '{0}.jpg'.format(self.classified_object_name())
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: '{0}_thumb.jpg'.format(self.classified_object_name())
            }
        ]

    # 原本的业务元数据质检
    # def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser):
    #     """
    #     初始化默认的, 业务元数据xml文件的检验列表
    #     :param parser:
    #     :return:
    #     """
    #     return [
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/OrbitID',
    #             self.Name_ID: 'OrbitID',
    #             self.Name_Title: '轨道编号',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_string
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/ProduceType',
    #             self.Name_ID: 'ProduceType',
    #             self.Name_Title: '产品类型',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_string
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/ProductLevel',
    #             self.Name_ID: 'ProductLevel',
    #             self.Name_Title: '产品属性',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_string
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/TopLeftLatitude',
    #             self.Name_ID: 'TopLeftLatitude',
    #             self.Name_Title: '左上角纬度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -90,
    #                     self.Name_Max: 90
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/TopLeftLongitude',
    #             self.Name_ID: 'TopLeftLongitude',
    #             self.Name_Title: '左上角经度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -180,
    #                     self.Name_Max: 180
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/TopRightLatitude',
    #             self.Name_ID: 'TopRightLatitude',
    #             self.Name_Title: '右上角纬度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -90,
    #                     self.Name_Max: 90
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/TopRightLongitude',
    #             self.Name_ID: 'TopRightLongitude',
    #             self.Name_Title: '右上角经度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -180,
    #                     self.Name_Max: 180
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/BottomRightLatitude',
    #             self.Name_ID: 'BottomRightLatitude',
    #             self.Name_Title: '右下角纬度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -90,
    #                     self.Name_Max: 90
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/BottomRightLongitude',
    #             self.Name_ID: 'BottomRightLongitude',
    #             self.Name_Title: '右下角经度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -180,
    #                     self.Name_Max: 180
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/BottomLeftLatitude',
    #             self.Name_ID: 'BottomLeftLatitude',
    #             self.Name_Title: '左下角纬度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -90,
    #                     self.Name_Max: 90
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/BottomLeftLongitude',
    #             self.Name_ID: 'BottomLeftLongitude',
    #             self.Name_Title: '左下角经度',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -180,
    #                     self.Name_Max: 180
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/ProduceTime',
    #             self.Name_ID: 'ProduceTime',
    #             self.Name_Title: '发布时间',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_datetime
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/StartTime',
    #             self.Name_ID: 'StartTime',
    #             self.Name_Title: '开始时间',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_datetime
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/EndTime',
    #             self.Name_ID: 'EndTime',
    #             self.Name_Title: '结束时间',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_datetime
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/ImageGSD',
    #             self.Name_ID: 'ImageGSD',
    #             self.Name_Title: '分辨率',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_integer
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/CenterTime',
    #             self.Name_ID: 'CenterTime',
    #             self.Name_Title: '影像获取时间',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_datetime
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/RollViewingAngle',
    #             self.Name_ID: 'RollViewingAngle',
    #             self.Name_Title: '侧摆角',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_Range:
    #                 {
    #                     self.Name_Min: -90,
    #                     self.Name_Max: 90
    #                 },
    #             self.Name_DataType: self.value_type_decimal
    #
    #         },
    #         {
    #             self.Name_Type: self.QA_Type_XML_Node_Exist,
    #             self.Name_XPath: '/ProductMetaData/CloudPercent',
    #             self.Name_ID: 'CloudPercent',
    #             self.Name_Title: '云量',
    #             self.Name_Group: self.QA_Group_Data_Integrity,
    #             self.Name_Result: self.QA_Result_Error,
    #             self.Name_DataType: self.value_type_decimal_or_integer
    #
    #         }
    #     ]
