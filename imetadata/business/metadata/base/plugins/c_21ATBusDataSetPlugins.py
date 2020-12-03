# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_3002_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class C21ATBusDataSetPlugins(CDirPlugins):
    __classified_object_type = None
    __metadata_xml_obj__ = None
    __bus_metadata_xml_file_name__ = None

    def get_information(self) -> dict:
        information = super().get_information()
        if self.__metadata_xml_obj__ is not None:
            information[self.Plugins_Info_Title] = CXml.get_element_text(
                self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductName))
        information[self.Plugins_Info_Type_Code] = None  # '110001'
        information[self.Plugins_Info_Group] = self.DataGroup_Industry_DataSet
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Land  # 'land'
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(
            information[self.Plugins_Info_Catalog])  # '国土行业'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_TagsEngine] = 'global_dim'
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_HasChildObj] = self.DB_True

        return information

    def classified(self):
        self._object_confirm = self.Object_Confirm_IUnKnown
        self._object_name = None

        current_path = self.file_info.file_name_with_full_path
        metadata_file_name = CFile.join_file(current_path, self.FileName_MetaData_Bus_21AT)
        if CFile.file_or_path_exist(metadata_file_name):
            self.__bus_metadata_xml_file_name__ = metadata_file_name
            self.__metadata_xml_obj__ = CXml()
            try:
                self.__metadata_xml_obj__.load_file(metadata_file_name)
                self.__classified_object_type = CXml.get_element_text(
                    self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductType))

                if CUtils.equal_ignore_case(
                        self.__classified_object_type,
                        CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Type, None)
                ):
                    self._object_confirm = self.Object_Confirm_IKnown
                    self._object_name = CXml.get_element_text(
                        self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductName)
                    )
            except:
                self.__metadata_xml_obj__ = None
                CLogger().warning('发现文件{0}符合二十一世纪业务数据集标准, 但该文件格式有误, 无法打开! ')

        return self._object_confirm, self._object_name

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        if not CFile.file_or_path_exist(self.__bus_metadata_xml_file_name__):
            return CResult.merge_result(self.Failure,
                                        '元数据文件[{0}]不存在, 无法解析! '.format(self.__bus_metadata_xml_file_name__))

        try:
            parser.metadata.set_metadata_bus_file(
                self.Success,
                '元数据文件[{0}]成功加载! '.format(self.__bus_metadata_xml_file_name__),
                self.MetaDataFormat_XML,
                self.__bus_metadata_xml_file_name__)
            return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(self.__bus_metadata_xml_file_name__))
        except:
            parser.metadata.set_metadata_bus(
                self.Failure,
                '元数据文件[{0}]格式不合法, 无法处理! '.format(self.__bus_metadata_xml_file_name__),
                self.MetaDataFormat_Text,
                '')
            return CResult.merge_result(self.Exception,
                                        '元数据文件[{0}]格式不合法, 无法处理! '.format(self.__bus_metadata_xml_file_name__))

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//DSName",
                self.Name_ID: 'DSName',
                self.Name_Title: 'DSName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//BeginDate",
                self.Name_ID: 'BeginDate',
                self.Name_Title: 'BeginDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//EndDate",
                self.Name_ID: 'EndDate',
                self.Name_Title: 'EndDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Date",
                self.Name_ID: 'Date',
                self.Name_Title: 'Date',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//RegionCode",
                self.Name_ID: 'RegionCode',
                self.Name_Title: 'RegionCode',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//RegionName",
                self.Name_ID: 'RegionName',
                self.Name_Title: 'RegionName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Resolution",
                self.Name_ID: 'Resolution',
                self.Name_Title: 'Resolution',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 10
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//MajorSource",
                self.Name_ID: 'MajorSource',
                self.Name_Title: 'MajorSource',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ScaleDenominator",
                self.Name_ID: 'ScaleDenominator',
                self.Name_Title: 'ScaleDenominator',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ProductType",
                self.Name_ID: 'ProductType',
                self.Name_Title: 'ProductType',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Remark",
                self.Name_ID: 'Remark',
                self.Name_Title: 'Remark',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 500
            }
        ]
