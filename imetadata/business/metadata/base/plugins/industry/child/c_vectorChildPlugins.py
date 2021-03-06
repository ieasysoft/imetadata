# -*- coding: utf-8 -*- 
# @Time : 2020/11/26 15:06 
# @Author : 王西亚 
# @File : c_vectorChildPlugins.py
from imetadata.business.metadata.base.plugins.industry.child.c_spatialChildPlugins import CSpatialChildPlugins


class CVectorChildPlugins(CSpatialChildPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        # information[self.Plugins_Info_Name] = 'vector_layer'
        information[self.Plugins_Info_Type] = 'vector_layer'
        information[self.Plugins_Info_Type_Title] = '矢量数据集图层'
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_Group] = self.DataGroup_Vector
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Spatial_Layer
        information[self.Plugins_Info_Is_Spatial] = self.DB_True
        information[self.Plugins_Info_Is_Dataset] = self.DB_False
        information[self.Plugins_Info_Spatial_Qa] = self.DB_True
        information[self.Plugins_Info_Time_Qa] = self.DB_True
        information[self.Plugins_Info_Visual_Qa] = self.DB_False

        return information
