# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:23
# @Author : 赵宇飞
# @File : distribution_guotu_dataset.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import \
    distribution_guotu
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_json import CJson
from imetadata.base.c_xml import CXml
import datetime


class distribution_guotu_dataset(distribution_guotu):
    """"
    数据集对象处理基类（即时服务）
    """

    def information(self) -> dict:
        info = super().information()
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        return self.get_sync_predefined_dict_list(insert_or_updata)

    def get_sync_predefined_dict_list(self, insert_or_updata) -> list:
        """
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = list()
        object_table_id = self._obj_id
        object_table_data = self._dataset
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'aprid', object_table_id, self.DB_True)

        dsometadataxml = object_table_data.value_by_name(0, 'dsometadataxml', '')
        dsometadataxml_xml = CXml.load_xml(dsometadataxml)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'productname',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/DSName'),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producttype', object_table_data.value_by_name(0, 'dsodcode', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsodatatype', object_table_data.value_by_name(0, 'dsodatatype', ''), self.DB_True)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/BeginDate'),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/EndDate'),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Date'),
            self.DB_True)
        # datacount:数据数量
        # secrecylevel:密级
        regioncode = dsometadataxml_xml.get_element_text_by_xpath_one('/root/RegionCode')
        self.add_value_to_sync_dict_list(  # regioncode:行政区码
            sync_dict_list, 'regioncode',
            regioncode,
            self.DB_True)
        self.add_value_to_sync_dict_list(  # regionname:行政区
            sync_dict_list, 'regionname',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/RegionName'),
            self.DB_True)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerx',
            "(select centerx from ro_global_dim_space "
            "where gdscode='{0}')".format(regioncode), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centery',
            "(select centery from ro_global_dim_space "
            "where gdscode='{0}')".format(regioncode), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomwkt',
            "st_astext("
            "(select gdsgeometry from ro_global_dim_space where gdscode='{0}')"
            ")".format(regioncode), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomobj',
            "(select gdsgeometry from ro_global_dim_space where gdscode='{0}')".format(regioncode),
            self.DB_False)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'browserimg', object_table_data.value_by_name(0, 'dso_browser', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'thumbimg', object_table_data.value_by_name(0, 'dso_thumb', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producetime',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Date'),
            self.DB_True)
        now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'addtime', now_time, self.DB_True)
        self.add_value_to_sync_dict_list(  # resolution:分辨率
            sync_dict_list, 'resolution',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Resolution'),
            self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'imgsize',
        #     "(select round((sum(dodfilesize)/1048576),2) from dm2_storage_obj_detail "
        #     "where dodobjectid='{0}')".format(object_table_id),
        #     self.DB_False)
        # # colormodel:交插件处理
        # # piexldepth:交插件处理
        # if insert_or_updata:
        #     self.add_value_to_sync_dict_list(
        #         sync_dict_list, 'isdel', '0', self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'extent',
        #     "(select dso_geo_bb_native from dm2_storage_object where dsoid='{0}')".format(object_table_id),
        #     self.DB_False)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'proj', object_table_data.value_by_name(0, 'dso_prj_coordinate', ''), self.DB_True)
        # # remark:暂时为空
        # # ispublishservice:暂时为空
        # if insert_or_updata:
        #     self.add_value_to_sync_dict_list(
        #         sync_dict_list, 'queryable', '1', self.DB_True)
        # # scale:交插件处理
        # # mainrssource:交插件处理
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'dsdid', object_table_data.value_by_name(0, 'query_directory_id', ''), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'dsfid', object_table_data.value_by_name(0, 'query_file_id', ''), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'imagedatetag', dso_time_json.xpath_one('time', ''), self.DB_True)

        return sync_dict_list
