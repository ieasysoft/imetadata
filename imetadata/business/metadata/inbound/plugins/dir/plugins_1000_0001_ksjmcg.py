# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.base.plugins.custom.c_dirPlugins_keyword import CDirPlugins_keyword


class plugins_1000_0001_ksjmcg(CDirPlugins_keyword):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津测绘'
        information[self.Plugins_Info_Catalog_Title] = '天津测绘'
        information[self.Plugins_Info_Group] = '中间成果'
        information[self.Plugins_Info_Group_Title] = '中间成果'
        information[self.Plugins_Info_Type] = '空三加密成果'
        information[self.Plugins_Info_Type_Title] = '空三加密成果'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.TextMatchType_Regex: '(?i)空三加密成果|空三加密'
            },
            {
                self.Name_ID: self.Name_FilePath,
                self.TextMatchType_Regex: None
            }
        ]

    def get_classified_character_of_affiliated_keyword(self):
        return []
