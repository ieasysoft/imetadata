# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:09
# @Author : 赵宇飞
# @File : distribution_object_third_survey.py
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_third_survey(distribution_guotu_object):
    """
    邢凯凯 数据检索分发模块对三调影像类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '三调影像'
        info['table_name'] = 'ap3_product_rsp_th3sur_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
                insert_or_updata 中 self.DB_True为insert，DB_False为updata
                本方法的写法为强规则，调用add_value_to_sync_dict_list配置
                第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict = self.get_sync_predefined_dict_list(insert_or_updata)
        object_table_id = self._obj_id
        object_table_data = self._dataset

        # 业务元数据
        dsometadataxml_bus = object_table_data.value_by_name(0, 'dsometadataxml_bus', '')
        xml = CXml()
        xml.load_xml(dsometadataxml_bus)

        # 后处理流程介绍文档中的字段
        if insert_or_updata:
            self.add_value_to_sync_dict_list(sync_dict, 'aprtdid', object_table_id)
        self.add_value_to_sync_dict_list(sync_dict, 'aprtwid', object_table_data.value_by_name(0, 'dsoparentobjid', ''))
        self.add_value_to_sync_dict_list(sync_dict, 'datatype', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="sjgs"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'demname', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="gcjz"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'metafilename', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="ysjwjm"]'))
        # numeric
        self.add_value_to_sync_dict_list(sync_dict, 'isfull', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="mfqk"]'), self.DB_False)
        self.add_value_to_sync_dict_list(sync_dict, 'ellipsoidtype', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="tqlx"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'projinfo', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="dtty"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'centerline', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="zyjx"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'zonetype', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="fdfs"]'))
        # int4
        self.add_value_to_sync_dict_list(sync_dict, 'zoneno', CUtils().to_integer(xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="gsklgtydh"]')), self.DB_False)
        self.add_value_to_sync_dict_list(sync_dict, 'coordinateunit', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mbii"]/item[@name="zbdw"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'dsometadatajson',
                                         object_table_data.value_by_name(0, 'dsometadataxml_bus', ''))
        self.add_value_to_sync_dict_list(sync_dict, 'demstandard',
                                         xml.get_element_text_by_xpath_one(
                                             '/root/property[@tablename="mbii"]/item[@name="gcjz"]'))
        self.add_value_to_sync_dict_list(sync_dict, 'createrorganize',
                                         xml.get_element_text_by_xpath_one(
                                             '/root/property[@tablename="mbii"]/item[@name="sjscdw"]'))
        # self.add_value_to_sync_dict_list(sync_dict, 'bandcount', xml.get_element_text_by_xpath_one(''))
        # self.add_value_to_sync_dict_list(sync_dict, 'bandname', xml.get_element_text_by_xpath_one(''))
        # self.add_value_to_sync_dict_list(sync_dict, 'cloudpercent', xml.get_element_text_by_xpath_one(''))
        # 数据量
        self.add_value_to_sync_dict_list(sync_dict, 'datacount',
                                         xml.get_element_text_by_xpath_one(
                                             '/root/property[@tablename="mbii"]/item[@name="sjl"]'),
                                         self.DB_False)
        # 密级
        self.add_value_to_sync_dict_list(sync_dict, 'secrecylevel',
                                         xml.get_element_text_by_xpath_one(
                                             '/root/property[@tablename="mbii"]/item[@name="mj"]'))
        # 行政区码
        self.add_value_to_sync_dict_list(sync_dict, 'regioncode',
                                         xml.get_element_text_by_xpath_one(
                                             '/root/property[@tablename="mbii"]/item[@name="xzqdm"]'))
        # 行政区
        self.add_value_to_sync_dict_list(sync_dict, 'regionname',
                                         xml.get_element_text_by_xpath_one(
                                             '/root/property[@tablename="mbii"]/item[@name="xmc"]'))
        # 产品时间
        # self.add_value_to_sync_dict_list(sync_dict, 'producetime', xml.get_element_text_by_xpath_one(''))
        # 分辨率 待提取
        #self.add_value_to_sync_dict_list(sync_dict, 'resolution', xml.get_element_text_by_xpath_one(''), self.DB_True)
        # 色彩模式
        # self.add_value_to_sync_dict_list(sync_dict, 'colormodel', xml.get_element_text_by_xpath_one(''))
        # 像素位数
        # self.add_value_to_sync_dict_list(sync_dict, 'piexldepth', xml.get_element_text_by_xpath_one(''))
        # 比例尺分母
        # self.add_value_to_sync_dict_list(sync_dict, 'scale', xml.get_element_text_by_xpath_one(''))
        # 主要星源
        self.add_value_to_sync_dict_list(sync_dict, 'mainrssource', xml.get_element_text_by_xpath_one(
            '/root/property[@tablename="mpid"]/item[@name="sjy"]'))
        # 备注
        # self.add_value_to_sync_dict_list(sync_dict, 'remark', xml.get_element_text_by_xpath_one(''))

        return sync_dict
