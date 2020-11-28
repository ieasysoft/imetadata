# -*- coding: utf-8 -*- 
# @Time : 2020/11/05 17:09
# @Author : 赵宇飞
# @File : plugins_9005_busdataset_third_survey.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9005_busdataset_third_survey(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-三调影像'
        information[self.Plugins_Info_Name] = '三调影像'
        # information[self.Plugins_Info_Type] = 'business_data_set_third_survey'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_Third_Survey
        information[self.Plugins_Info_Code] = '020104'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset_Business
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_third_survey'
        return information