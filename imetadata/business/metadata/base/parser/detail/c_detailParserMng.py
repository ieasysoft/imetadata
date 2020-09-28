# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 14:11 
# @Author : 王西亚 
# @File : c_detailParserMng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.detail.c_detailParser_all_file_of_dir import CDetailParser_All_File_Of_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_all_file_of_same_dir import \
    CDetailParser_All_File_Of_Same_Dir
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.detail.c_detailParser_file_of_dir import CDetailParser_File_Of_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_file_of_same_dir import \
    CDetailParser_File_Of_Same_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_same_file_main_name import \
    CDetailParser_Same_File_Main_Name


class CDetailParserMng(CResource):
    @classmethod
    def give_me_parser(cls, parser_type, object_id: str, object_name: str, file_info: CDMFilePathInfoEx):
        input_parser_type = CUtils.any_2_str(parser_type)

        if CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_Same_File_Main_Name):
            return CDetailParser_Same_File_Main_Name(object_id, object_name, file_info)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_File_Of_Same_Dir):
            return CDetailParser_File_Of_Same_Dir(object_id, object_name, file_info)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_All_File_Of_Same_Dir):
            return CDetailParser_All_File_Of_Same_Dir(object_id, object_name, file_info)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_File_Of_Dir):
            return CDetailParser_File_Of_Dir(object_id, object_name, file_info)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_All_File_Of_Dir):
            return CDetailParser_All_File_Of_Dir(object_id, object_name, file_info)
        else:
            return CParserCustom(object_id, object_name, file_info)
