# -*- coding: utf-8 -*- 
# @Time : 2020/9/27 10:15 
# @Author : 王西亚 
# @File : c_audit.py
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class CAudit(CResource):
    @classmethod
    def __init_audit_dict__(cls, audit_id, audit_title, audit_type) -> dict:
        result_dict = dict()
        result_dict[cls.Name_ID] = audit_id
        result_dict[cls.Name_Title] = audit_title
        result_dict[cls.Name_Type] = audit_type

        return result_dict

    @classmethod
    def a_file_exist(cls, audit_id, audit_title, audit_type, file_name_with_path) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_type)

        if CFile.file_or_path_exist(file_name_with_path):
            result_dict[cls.Name_Message] = '文件[{0}]存在, 符合要求'.format(CFile.file_name(file_name_with_path))
            result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
        else:
            result_dict[cls.Name_Message] = '文件[{0}]不存在, 请检查'.format(CFile.file_name(file_name_with_path))

        return result_dict

    @classmethod
    def a_file_size(cls, audit_id, audit_title, audit_type, file_name_with_path: str, size_min: int = -1,
                    size_max: int = -1) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_type)

        file_size = CFile.file_size(file_name_with_path)

        if size_min != -1 and size_min != -1:
            if size_min <= file_size <= size_max:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]在指定的[{2}-{3}]范围内, 符合要求!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_min,
                    size_max)
                result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]在指定的[{2}-{3}]范围外, 请检查!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_min,
                    size_max)
        elif size_min != -1:
            if size_min <= file_size:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]大于最小值[{2}], 符合要求!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_min)
                result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]低于最小值[{2}], 请检查!'.format(
                    CFile.file_name(file_name_with_path), file_size,
                    size_min)
        elif size_max != -1:
            if size_max >= file_size:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]低于最大值[{2}], 符合要求!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_max)
                result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]超过最大值[{2}], 请检查!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_max)
        else:
            result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]未给定限定范围, 默认符合要求!'.format(
                CFile.file_name(file_name_with_path), file_size)
            result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass

        return result_dict

    @classmethod
    def a_xml_element_exist(cls, audit_id, audit_title, audit_type, xml_obj: CXml, xpath: str) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_type)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return result_dict

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]存在, 符合要求!'.format(xpath)
            result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)

        return result_dict

    @classmethod
    def a_xml_element_text_in_list(cls, audit_id, audit_title, audit_type, xml_obj: CXml, xpath: str,
                                   value_list: list) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_type)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return result_dict

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            element_text = CXml.get_element_text(element_obj)
            if CUtils.list_count(value_list, element_text) > 0:
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]的值在指定列表中, 符合要求!'.format(xpath)
                result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
            else:
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]的值[{1}], 不在指定列表中, 请检查修正!'.format(xpath, element_text)
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)

        return result_dict

    @classmethod
    def a_xml_attr_exist(cls, audit_id, audit_title, audit_type, xml_obj: CXml, xpath: str, attr_name: str) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_type)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return result_dict

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            if CXml.attr_exist(element_obj, attr_name):
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]存在属性[{1}], 符合要求!'.format(xpath, attr_name)
                result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
            else:
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]无属性[{1}], 请检查修正!'.format(xpath, attr_name)
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)

        return result_dict

    @classmethod
    def a_xml_attr_value_in_list(cls, audit_id, audit_title, audit_type, xml_obj: CXml, xpath: str, attr_name: str,
                                 value_list: list) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_type)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return result_dict

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            if CXml.attr_exist(element_obj, attr_name):
                attr_text = CXml.get_attr(element_obj, attr_name, '')
                if CUtils.list_count(value_list, attr_text) > 0:
                    result_dict[cls.Name_Message] = 'XML对象的节点[{0}]存在属性[{1}], 符合要求!'.format(xpath, attr_name)
                    result_dict[cls.Name_Type] = cls.QualityAudit_Type_Pass
                else:
                    result_dict[cls.Name_Message] = 'XML对象的节点[{0}]的值[{1}], 不在指定列表中, 请检查修正!'.format(xpath, attr_text)
            else:
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]无属性[{1}], 请检查修正!'.format(xpath, attr_name)
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)

        return result_dict