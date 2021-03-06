# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_4004_gf1b import plugins_4004_gf1b
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("GF1B压缩包类型成果影像")  # 模块标题
class Test_plugins_4004_gf1b_file(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4004_gf1b(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'GF1B_PMS_E117.1_N30.2_20190121_L1A1227579261.tar.gz',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF1B_PMS_E117.1_N30.2_20190121_L1A1227579261'
            }
        ]


if __name__ == '__main__':
    pytest.main()
