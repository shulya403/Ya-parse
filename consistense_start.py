import consistence_parsed_names as CPN

#May = CPN.Concat_Parse_Files('Ноутбук')
#May.Concat_files()

#class Consist_Names(object):

#    def __init__(self,
#                 category,
#                 file_itr,
#                 file_itr_page="",
#                 itr_model_field="",
#                 itr_vendor_field="",
#                 JSON_file="cons_parsed_files.json",
#                 M='May',
#                 Y=20,
#                 file_work_name = "",
#                 file_base_name = "",
#                 dir_root="Prices/",
#                 dir_work="Handle_base/",
#                 ):


FileHandler = CPN.Consist_Names(category="Ноутбук",
                                file_itr="NB_Pivot_Mar (Восстановленный).xlsm",
                                file_work_name="Ноутбук-Concat_Prices--May-20--Filled3.xlsx")
#FileHandler.Fill_Work_by_Base()

#   Заполенение из файла Source
#FileHandler.Fill_Unknown()
FileHandler.Dict_Yama_Names()
print(FileHandler.dict_yama_names)

FileHandler.Fill_Yama_Name()

#   Заполенение фала Base Stable проверенными
#FileHandler.Checked_To_Base('Ноутбук', 'Ноутбук-Concat_Prices--May-20--Checked.xlsx')