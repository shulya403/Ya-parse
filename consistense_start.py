import consistence_parsed_names as CPN

#   ----------
#   CPN.Concat_Parse_Files соединяет месячные файлы прайсов пробегая по директорям сайтов.
#Формирует файл ..._Source в Handle/
#   CPN Consist_Names заполняет поле Name в фале file_work_name (_Source) именами из поля json-cons-parsed-files:"itr-file":"models_field"
#проверяя на соответсвие STRadar с полем Modification_name
#Записи Name имеющиеся в Handle_base заливаются из него (Known=True)
#   CPN.Fill_Stable_Base дополняет Stable_base Ложными (Known) и Ok=1 в прочищенном файле Checked.
#Совпадения заменяются новыми из Checked
#   ----------


#May = CPN.Concat_Parse_Files('Монитор')
#May.Concat_files()
#May.Clearing_Vendors()
#May.Clearing_Mod_Name()

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


FileHandler = CPN.Consist_Names(category="Монитор",
                                file_itr="Monitors all models drop_duplicates.xlsx",
                                file_work_name="")


#   Заполенение из файла Source
FileHandler.Fill_Unknown()

#FileHandler.Dict_Yama_Names()
#FileHandler.Fill_Yama_Name()




#   Заполенение фала Base Stable проверенными


#StBase = CPN.Fill_Stable_Base('Ноутбук',
#                              'Ноутбук-Concat_Prices--May-20--Checked2.xlsx')
#StBase.Checked_To_Base()