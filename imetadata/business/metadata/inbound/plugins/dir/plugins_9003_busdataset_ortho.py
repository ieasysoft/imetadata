# -*- coding: utf-8 -*- 
# @Time : 2020/11/05 17:08
# @Author : 赵宇飞
# @File : plugins_9003_busdataset_ortho.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9003_busdataset_ortho(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '单景正射数据集'
        information[self.Plugins_Info_Code] = '020101'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_ortho'
        return information