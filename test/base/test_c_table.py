# -*- coding: utf-8 -*- 
# @Time : 2020/11/26 08:44 
# @Author : 王西亚 
# @File : test_c_table.py

import allure
import pytest
from imetadata.base.c_resource import CResource
from imetadata.database.tools.c_table import CTable


class Test_C_Table:

    @allure.title('测试单表入库')
    def test_all(self):
        table = CTable()
        table.load_info(CResource.DB_Server_ID_Default, 'dm2_storage_object')
        table.column_list.column_by_name('dsoid').set_value('dsoid')
        table.column_list.column_by_name('dsoobjectname').set_value('dsoobjectname')
        table.column_list.column_by_name('dsoobjecttype').set_value('dsoobjecttype')
        table.column_list.column_by_name('dsodatatype').set_value('dsodatatype')
        table.column_list.column_by_name('dsoalphacode').set_value('dsoalphacode')

        table.column_list.column_by_name('dso_obj_lastmodifytime').set_sql('now()')
        table.delete_data()
        table.insert_data()
        if table.if_exists():
            print('row create success')
        else:
            print('row create failure')

        table.column_list.column_by_name('dsoobjectname').set_value('dsoobjectname_update')

        table.column_list.column_by_name('dsometadataxml').set_value('''
<root><test name="中国"/></root>
            ''')
        table.column_list.column_by_name('dsometadatajson').set_value('''
        {"size": {"width": 10020, "height": 5010}, "bands": [{"mask": {"valid": true}, "type": "Byte", "block": {"width": 10020, "height": 1}, "scale": null, "offset": null, "metadata": [], "color_table": {"entrys": [{"color1": 255, "color2": 255, "color3": 255, "color4": 255}, {"color1": 47, "color2": 89, "color3": 74, "color4": 255}, {"color1": 237, "color2": 247, "color3": 252, "color4": 255}, {"color1": 217, "color2": 232, "color3": 252, "color4": 255}, {"color1": 220, "color2": 217, "color3": 239, "color4": 255}, {"color1": 238, "color2": 231, "color3": 232, "color4": 255}, {"color1": 176, "color2": 208, "color3": 252, "color4": 255}, {"color1": 165, "color2": 116, "color3": 144, "color4": 255}, {"color1": 20, "color2": 80, "color3": 152, "color4": 255}, {"color1": 218, "color2": 215, "color3": 217, "color4": 255}, {"color1": 173, "color2": 197, "color3": 222, "color4": 255}, {"color1": 231, "color2": 243, "color3": 243, "color4": 255}, {"color1": 172, "color2": 146, "color3": 117, "color4": 255}, {"color1": 113, "color2": 121, "color3": 134, "color4": 255}, {"color1": 73, "color2": 77, "color3": 54, "color4": 255}, {"color1": 164, "color2": 200, "color3": 209, "color4": 255}, {"color1": 13, "color2": 72, "color3": 145, "color4": 255}, {"color1": 166, "color2": 167, "color3": 195, "color4": 255}, {"color1": 0, "color2": 49, "color3": 121, "color4": 255}, {"color1": 163, "color2": 174, "color3": 160, "color4": 255}, {"color1": 19, "color2": 62, "color3": 125, "color4": 255}, {"color1": 196, "color2": 213, "color3": 199, "color4": 255}, {"color1": 106, "color2": 69, "color3": 57, "color4": 255}, {"color1": 108, "color2": 144, "color3": 199, "color4": 255}, {"color1": 96, "color2": 94, "color3": 64, "color4": 255}, {"color1": 49, "color2": 75, "color3": 43, "color4": 255}, {"color1": 100, "color2": 75, "color3": 84, "color4": 255}, {"color1": 83, "color2": 129, "color3": 72, "color4": 255}, {"color1": 139, "color2": 118, "color3": 99, "color4": 255}, {"color1": 40, "color2": 90, "color3": 49, "color4": 255}, {"color1": 31, "color2": 95, "color3": 165, "color4": 255}, {"color1": 69, "color2": 110, "color3": 99, "color4": 255}, {"color1": 112, "color2": 95, "color3": 88, "color4": 255}, {"color1": 75, "color2": 106, "color3": 62, "color4": 255}, {"color1": 28, "color2": 61, "color3": 31, "color4": 255}, {"color1": 60, "color2": 128, "color3": 63, "color4": 255}, {"color1": 40, "color2": 23, "color3": 18, "color4": 255}, {"color1": 251, "color2": 251, "color3": 254, "color4": 255}, {"color1": 50, "color2": 113, "color3": 55, "color4": 255}, {"color1": 17, "color2": 68, "color3": 24, "color4": 255}, {"color1": 96, "color2": 107, "color3": 89, "color4": 255}, {"color1": 178, "color2": 166, "color3": 125, "color4": 255}, {"color1": 140, "color2": 163, "color3": 148, "color4": 255}, {"color1": 30, "color2": 67, "color3": 111, "color4": 255}, {"color1": 33, "color2": 81, "color3": 39, "color4": 255}, {"color1": 25, "color2": 42, "color3": 21, "color4": 255}, {"color1": 0, "color2": 40, "color3": 102, "color4": 255}, {"color1": 74, "color2": 109, "color3": 46, "color4": 255}, {"color1": 71, "color2": 93, "color3": 54, "color4": 255}, {"color1": 62, "color2": 113, "color3": 62, "color4": 255}, {"color1": 97, "color2": 138, "color3": 77, "color4": 255}, {"color1": 6, "color2": 62, "color3": 136, "color4": 255}, {"color1": 91, "color2": 114, "color3": 104, "color4": 255}, {"color1": 63, "color2": 100, "color3": 58, "color4": 255}, {"color1": 42, "color2": 107, "color3": 176, "color4": 255}, {"color1": 38, "color2": 108, "color3": 53, "color4": 255}, {"color1": 70, "color2": 121, "color3": 66, "color4": 255}, {"color1": 112, "color2": 134, "color3": 81, "color4": 255}, {"color1": 81, "color2": 172, "color3": 88, "color4": 255}, {"color1": 135, "color2": 114, "color3": 80, "color4": 255}, {"color1": 1, "color2": 28, "color3": 81, "color4": 255}, {"color1": 7, "color2": 76, "color3": 131, "color4": 255}, {"color1": 41, "color2": 49, "color3": 28, "color4": 255}, {"color1": 162, "color2": 127, "color3": 101, "color4": 255}, {"color1": 186, "color2": 186, "color3": 113, "color4": 255}, {"color1": 116, "color2": 113, "color3": 76, "color4": 255}, {"color1": 64, "color2": 131, "color3": 199, "color4": 255}, {"color1": 188, "color2": 160, "color3": 148, "color4": 255}, {"color1": 192, "color2": 167, "color3": 126, "color4": 255}, {"color1": 93, "color2": 156, "color3": 92, "color4": 255}, {"color1": 158, "color2": 140, "color3": 92, "color4": 255}, {"color1": 168, "color2": 149, "color3": 104, "color4": 255}, {"color1": 176, "color2": 135, "color3": 107, "color4": 255}, {"color1": 230, "color2": 201, "color3": 154, "color4": 255}, {"color1": 86, "color2": 108, "color3": 68, "color4": 255}, {"color1": 129, "color2": 83, "color3": 63, "color4": 255}, {"color1": 57, "color2": 83, "color3": 58, "color4": 255}, {"color1": 208, "color2": 181, "color3": 139, "color4": 255}, {"color1": 160, "color2": 129, "color3": 84, "color4": 255}, {"color1": 127, "color2": 138, "color3": 97, "color4": 255}, {"color1": 237, "color2": 217, "color3": 162, "color4": 255}, {"color1": 220, "color2": 188, "color3": 148, "color4": 255}, {"color1": 110, "color2": 89, "color3": 61, "color4": 255}, {"color1": 165, "color2": 169, "color3": 111, "color4": 255}, {"color1": 99, "color2": 101, "color3": 57, "color4": 255}, {"color1": 205, "color2": 190, "color3": 154, "color4": 255}, {"color1": 141, "color2": 139, "color3": 104, "color4": 255}, {"color1": 241, "color2": 220, "color3": 177, "color4": 255}, {"color1": 108, "color2": 165, "color3": 105, "color4": 255}, {"color1": 103, "color2": 113, "color3": 67, "color4": 255}, {"color1": 7, "color2": 29, "color3": 5, "color4": 255}, {"color1": 90, "color2": 104, "color3": 121, "color4": 255}, {"color1": 188, "color2": 149, "color3": 113, "color4": 255}, {"color1": 57, "color2": 86, "color3": 48, "color4": 255}, {"color1": 222, "color2": 152, "color3": 124, "color4": 255}, {"color1": 22, "color2": 93, "color3": 35, "color4": 255}, {"color1": 75, "color2": 142, "color3": 69, "color4": 255}, {"color1": 253, "color2": 243, "color3": 193, "color4": 255}, {"color1": 89, "color2": 59, "color3": 41, "color4": 255}, {"color1": 106, "color2": 183, "color3": 105, "color4": 255}, {"color1": 85, "color2": 155, "color3": 220, "color4": 255}, {"color1": 0, "color2": 17, "color3": 62, "color4": 255}, {"color1": 53, "color2": 119, "color3": 187, "color4": 255}, {"color1": 3, "color2": 7, "color3": 2, "color4": 255}, {"color1": 239, "color2": 233, "color3": 200, "color4": 255}, {"color1": 14, "color2": 32, "color3": 12, "color4": 255}, {"color1": 86, "color2": 84, "color3": 62, "color4": 255}, {"color1": 143, "color2": 150, "color3": 91, "color4": 255}, {"color1": 38, "color2": 58, "color3": 53, "color4": 255}, {"color1": 47, "color2": 133, "color3": 68, "color4": 255}, {"color1": 91, "color2": 163, "color3": 227, "color4": 255}, {"color1": 69, "color2": 48, "color3": 32, "color4": 255}, {"color1": 144, "color2": 168, "color3": 103, "color4": 255}, {"color1": 106, "color2": 177, "color3": 120, "color4": 255}, {"color1": 22, "color2": 13, "color3": 8, "color4": 255}, {"color1": 75, "color2": 87, "color3": 64, "color4": 255}, {"color1": 168, "color2": 212, "color3": 151, "color4": 255}, {"color1": 90, "color2": 168, "color3": 98, "color4": 255}, {"color1": 37, "color2": 63, "color3": 39, "color4": 255}, {"color1": 65, "color2": 148, "color3": 80, "color4": 255}, {"color1": 7, "color2": 52, "color3": 13, "color4": 255}, {"color1": 15, "color2": 75, "color3": 41, "color4": 255}, {"color1": 0, "color2": 18, "color3": 43, "color4": 255}, {"color1": 38, "color2": 84, "color3": 120, "color4": 255}, {"color1": 23, "color2": 88, "color3": 48, "color4": 255}, {"color1": 98, "color2": 102, "color3": 76, "color4": 255}, {"color1": 94, "color2": 143, "color3": 90, "color4": 255}, {"color1": 109, "color2": 120, "color3": 100, "color4": 255}, {"color1": 40, "color2": 76, "color3": 56, "color4": 255}, {"color1": 43, "color2": 60, "color3": 78, "color4": 255}, {"color1": 38, "color2": 100, "color3": 46, "color4": 255}, {"color1": 44, "color2": 92, "color3": 150, "color4": 255}, {"color1": 48, "color2": 42, "color3": 27, "color4": 255}, {"color1": 67, "color2": 117, "color3": 177, "color4": 255}, {"color1": 91, "color2": 126, "color3": 83, "color4": 255}, {"color1": 59, "color2": 98, "color3": 77, "color4": 255}, {"color1": 22, "color2": 78, "color3": 143, "color4": 255}, {"color1": 114, "color2": 158, "color3": 223, "color4": 255}, {"color1": 72, "color2": 134, "color3": 76, "color4": 255}, {"color1": 17, "color2": 42, "color3": 107, "color4": 255}, {"color1": 59, "color2": 127, "color3": 108, "color4": 255}, {"color1": 59, "color2": 128, "color3": 165, "color4": 255}, {"color1": 69, "color2": 92, "color3": 99, "color4": 255}, {"color1": 123, "color2": 151, "color3": 104, "color4": 255}, {"color1": 76, "color2": 123, "color3": 103, "color4": 255}, {"color1": 70, "color2": 78, "color3": 41, "color4": 255}, {"color1": 148, "color2": 130, "color3": 113, "color4": 255}, {"color1": 97, "color2": 119, "color3": 69, "color4": 255}, {"color1": 81, "color2": 98, "color3": 65, "color4": 255}, {"color1": 123, "color2": 124, "color3": 85, "color4": 255}, {"color1": 105, "color2": 149, "color3": 95, "color4": 255}, {"color1": 123, "color2": 100, "color3": 74, "color4": 255}, {"color1": 142, "color2": 130, "color3": 84, "color4": 255}, {"color1": 148, "color2": 114, "color3": 70, "color4": 255}, {"color1": 20, "color2": 82, "color3": 26, "color4": 255}, {"color1": 198, "color2": 147, "color3": 103, "color4": 255}, {"color1": 206, "color2": 163, "color3": 117, "color4": 255}, {"color1": 80, "color2": 29, "color3": 38, "color4": 255}, {"color1": 24, "color2": 56, "color3": 84, "color4": 255}, {"color1": 168, "color2": 114, "color3": 82, "color4": 255}, {"color1": 189, "color2": 143, "color3": 96, "color4": 255}, {"color1": 51, "color2": 110, "color3": 127, "color4": 255}, {"color1": 159, "color2": 143, "color3": 118, "color4": 255}, {"color1": 49, "color2": 38, "color3": 52, "color4": 255}, {"color1": 38, "color2": 68, "color3": 28, "color4": 255}, {"color1": 227, "color2": 209, "color3": 173, "color4": 255}, {"color1": 175, "color2": 173, "color3": 139, "color4": 255}, {"color1": 178, "color2": 191, "color3": 147, "color4": 255}, {"color1": 51, "color2": 98, "color3": 53, "color4": 255}, {"color1": 133, "color2": 161, "color3": 123, "color4": 255}, {"color1": 187, "color2": 161, "color3": 106, "color4": 255}, {"color1": 62, "color2": 58, "color3": 46, "color4": 255}, {"color1": 72, "color2": 141, "color3": 207, "color4": 255}, {"color1": 52, "color2": 61, "color3": 27, "color4": 255}, {"color1": 90, "color2": 80, "color3": 48, "color4": 255}, {"color1": 124, "color2": 172, "color3": 104, "color4": 255}, {"color1": 121, "color2": 155, "color3": 89, "color4": 255}, {"color1": 85, "color2": 96, "color3": 78, "color4": 255}, {"color1": 88, "color2": 195, "color3": 84, "color4": 255}, {"color1": 108, "color2": 152, "color3": 126, "color4": 255}, {"color1": 104, "color2": 116, "color3": 89, "color4": 255}, {"color1": 154, "color2": 176, "color3": 140, "color4": 255}, {"color1": 98, "color2": 127, "color3": 116, "color4": 255}, {"color1": 204, "color2": 217, "color3": 178, "color4": 255}, {"color1": 59, "color2": 74, "color3": 69, "color4": 255}, {"color1": 46, "color2": 77, "color3": 103, "color4": 255}, {"color1": 71, "color2": 80, "color3": 108, "color4": 255}, {"color1": 125, "color2": 187, "color3": 197, "color4": 255}, {"color1": 154, "color2": 188, "color3": 200, "color4": 255}, {"color1": 126, "color2": 140, "color3": 165, "color4": 255}, {"color1": 175, "color2": 229, "color3": 253, "color4": 255}, {"color1": 141, "color2": 204, "color3": 207, "color4": 255}, {"color1": 174, "color2": 218, "color3": 228, "color4": 255}, {"color1": 204, "color2": 231, "color3": 238, "color4": 255}, {"color1": 125, "color2": 151, "color3": 187, "color4": 255}, {"color1": 199, "color2": 251, "color3": 255, "color4": 255}, {"color1": 132, "color2": 172, "color3": 183, "color4": 255}, {"color1": 167, "color2": 210, "color3": 224, "color4": 255}, {"color1": 184, "color2": 228, "color3": 232, "color4": 255}, {"color1": 216, "color2": 251, "color3": 253, "color4": 255}, {"color1": 185, "color2": 234, "color3": 244, "color4": 255}, {"color1": 90, "color2": 146, "color3": 186, "color4": 255}, {"color1": 172, "color2": 226, "color3": 242, "color4": 255}, {"color1": 160, "color2": 190, "color3": 196, "color4": 255}, {"color1": 103, "color2": 157, "color3": 182, "color4": 255}, {"color1": 201, "color2": 244, "color3": 244, "color4": 255}, {"color1": 192, "color2": 239, "color3": 251, "color4": 255}, {"color1": 158, "color2": 227, "color3": 254, "color4": 255}, {"color1": 168, "color2": 216, "color3": 233, "color4": 255}, {"color1": 105, "color2": 144, "color3": 171, "color4": 255}, {"color1": 187, "color2": 225, "color3": 222, "color4": 255}, {"color1": 179, "color2": 248, "color3": 255, "color4": 255}, {"color1": 188, "color2": 155, "color3": 177, "color4": 255}, {"color1": 83, "color2": 112, "color3": 143, "color4": 255}, {"color1": 193, "color2": 191, "color3": 202, "color4": 255}, {"color1": 159, "color2": 188, "color3": 209, "color4": 255}, {"color1": 201, "color2": 210, "color3": 221, "color4": 255}, {"color1": 135, "color2": 173, "color3": 197, "color4": 255}, {"color1": 105, "color2": 133, "color3": 184, "color4": 255}, {"color1": 136, "color2": 189, "color3": 217, "color4": 255}, {"color1": 112, "color2": 160, "color3": 171, "color4": 255}, {"color1": 108, "color2": 220, "color3": 255, "color4": 255}, {"color1": 221, "color2": 253, "color3": 227, "color4": 255}, {"color1": 13, "color2": 42, "color3": 73, "color4": 255}, {"color1": 150, "color2": 198, "color3": 230, "color4": 255}, {"color1": 148, "color2": 215, "color3": 235, "color4": 255}, {"color1": 149, "color2": 159, "color3": 189, "color4": 255}, {"color1": 147, "color2": 180, "color3": 214, "color4": 255}, {"color1": 115, "color2": 144, "color3": 181, "color4": 255}, {"color1": 227, "color2": 255, "color3": 255, "color4": 255}, {"color1": 146, "color2": 202, "color3": 252, "color4": 255}, {"color1": 141, "color2": 185, "color3": 235, "color4": 255}, {"color1": 35, "color2": 119, "color3": 138, "color4": 255}, {"color1": 95, "color2": 150, "color3": 172, "color4": 255}, {"color1": 227, "color2": 246, "color3": 218, "color4": 255}, {"color1": 62, "color2": 95, "color3": 140, "color4": 255}, {"color1": 54, "color2": 88, "color3": 115, "color4": 255}, {"color1": 156, "color2": 169, "color3": 179, "color4": 255}, {"color1": 109, "color2": 126, "color3": 153, "color4": 255}, {"color1": 174, "color2": 211, "color3": 212, "color4": 255}, {"color1": 132, "color2": 171, "color3": 211, "color4": 255}, {"color1": 151, "color2": 182, "color3": 192, "color4": 255}, {"color1": 128, "color2": 164, "color3": 187, "color4": 255}, {"color1": 93, "color2": 133, "color3": 162, "color4": 255}, {"color1": 120, "color2": 176, "color3": 205, "color4": 255}, {"color1": 104, "color2": 159, "color3": 197, "color4": 255}, {"color1": 10, "color2": 16, "color3": 89, "color4": 255}, {"color1": 95, "color2": 139, "color3": 206, "color4": 255}, {"color1": 85, "color2": 110, "color3": 184, "color4": 255}, {"color1": 147, "color2": 162, "color3": 214, "color4": 255}, {"color1": 110, "color2": 214, "color3": 115, "color4": 255}, {"color1": 150, "color2": 92, "color3": 94, "color4": 255}, {"color1": 209, "color2": 176, "color3": 176, "color4": 255}, {"color1": 147, "color2": 193, "color3": 128, "color4": 255}, {"color1": 211, "color2": 188, "color3": 180, "color4": 255}, {"color1": 0, "color2": 0, "color3": 0, "color4": 255}], "entry_count": 256, "palette_interpretation_name": "RGB"}, "color_interp": "Palette", "image_structure_metadata": []}], "files": ["/Users/wangxiya/Documents/我的测试数据/11.入库存储/广西影像数据/2772.0-509.0/2772.0-509.0.tif"], "wgs84": {"msg": "boundingbox四至范围从WGS_1984坐标系转wgs_84坐标系转换成功！", "coordinate": {"wkt": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AXIS[\"Latitude\",NORTH],AXIS[\"Longitude\",EAST],AUTHORITY[\"EPSG\",\"4326\"]]", "esri": "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", "proj4": "+proj=longlat +datum=WGS84 +no_defs"}, "boundingbox": {"top": 89.99999999995, "left": -179.99999899994998, "right": 179.99999887005004, "bottom": -89.99999993704998}}, "driver": {"longname": "GeoTIFF", "shortname": "GTiff"}, "origin": {"geotransform0": -179.99999899994998, "geotransform3": 89.99999999995}, "result": -1, "pyramid": 0, "metadata": ["Area", "2 (pixels/inch)", "IMAGINE TIFF Support\nCopyright 1991 - 1999 by ERDAS, Inc. All Rights Reserved\n@(#)$RCSfile: etif.c $ $Revision: 1.9.1.2 $ $Date: 2001/12/05 00:33:12Z $", "1", "1"], "pixelsize": {"width": 0.0359281435, "height": -0.0359281437}, "coordinate": {"wkt": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AXIS[\"Latitude\",NORTH],AXIS[\"Longitude\",EAST],AUTHORITY[\"EPSG\",\"4326\"]]", "esri": "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", "proj4": "+proj=longlat +datum=WGS84 +no_defs"}, "boundingbox": {"top": 89.99999999995, "left": -179.99999899994998, "right": 179.99999887005004, "bottom": -89.99999993704998}, "corner_coordinates": {"center": {"x": 5010.0, "y": 2505.0}, "lower_left": {"x": 0, "y": 5010}, "upper_left": {"x": 0, "y": 0}, "lower_right": {"x": 10020, "y": 5010}, "upper_right": {"x": 10020, "y": 0}}, "image_structure_metadata": ["BAND"]}
            ''')
        table.column_list.column_by_name('dsotags').set_array(list([1, 2, 3]))

        table.column_list.column_by_name('dso_geo_wgs84').set_value(
            'POLYGON((-179.99999899995 89.99999999995,179.99999887005 89.99999999995,179.99999887005 -89.99999993705,-179.99999899995 -89.99999993705,-179.99999899995 89.99999999995))')
        table.update_data()
        print('row update success')
        assert True
