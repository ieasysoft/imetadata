# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_8020_ortho import plugins_8020_ortho
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("单景影像")  # 模块标题
class Test_Plugins_8020_Ortho(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_8020_ortho(file_info)

    def file_name_with_rel_path_list(self):
        return [
            (
                self.FileType_File,
                '单景test{0}单景test.tif'.format(CFile.sep()),
                -1,
                '单景test'
            ),
            (
                self.FileType_File,
                '单景test_123{0}单景test_123.tif'.format(CFile.sep()),
                -1,
                '单景test_123'
            ),
            (
                self.FileType_File,
                '单景test{0}单景test_21at.xml'.format(CFile.sep()),
                2,
                None
            )
        ]


if __name__ == '__main__':
    pytest.main()
