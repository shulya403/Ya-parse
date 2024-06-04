import consistence_parsed_names as CPN

#   ----------
#   CPN.Concat_Parse_Files соединяет месячные файлы прайсов пробегая по директорям сайтов.
# метод Concat_Files() Формирует файл ..._Source в Handle/
# ищет файлы по указанной категории с приставкой 'final.xlsx' для указанного месяца (M) и года (Y)

#   CPN Consist_Names заполняет поле Name в фале file_work_name (_Source) именами из поля json-cons-parsed-files:"itr-file":"models_field"
#проверяя на соответсвие STRadar с полем Modification_name
#Записи Name имеющиеся в Handle_base заливаются из него (Known=True)
#   CPN.Fill_Stable_Base дополняет Stable_base Ложными (Known) и Ok=1 в прочищенном файле Checked.
#Совпадения заменяются новыми из Checked
#   ----------
#Consist_Names_for_mth_report заполняет модели для месячных отчетов по ноутам Pivot


#def __init__(self,
#             category,
#             M='May',
#             Y=20,
#             JSON_file="cons_parsed_files.json",
#             dir_root="Prices/",
#             dir_work="Handle_base/"):

# May = CPN.Concat_Parse_Files('ноутбук', M='May', Y=24)
# May.Concat_files()


# May = CPN.Concat_Parse_Files('монитор', M='May', Y=24)
# May.Concat_files()

# #May.Clearing_Vendors() #Унификация имен вендоров в поле Vendor. Вызывается Concat_Files() или отдельно
#May.Clearing_Mod_Name() #Удаление имни вендора из Midification_name. Вызывается Concat_Files() или отдельно

#class Consist_Names(object):

#    def __init__(self,
#                 category,
#                 file_itr, #Файл с актуальым перечнем названий модлей. Из отчетных файлов
#                 file_itr_page="",
#                 itr_model_field="",
#                 itr_vendor_field="",
#                 JSON_file="cons_parsed_files.json",
#                 M='May',
#                 Y=20,
#                 file_work_name = "", # По умолчанию ищет файл c именем содержащим '_source', месяц (M) и категорию (category)
#                 file_base_name = "", #Файл Stable по категории
#                 dir_root="Prices/",
#                 dir_work="Handle_base/",
#                 ):

# FileHandler = CPN.Consist_Names(category="Монитор", #_Source для ноутов для yama заменить Mod_Name_restrict на просто Modification_name
#                                 file_itr="Reports/Monitors_Model_Base_2023_03-1.xlsx",
#                                 M='May',
#                                 Y='24',
#                                 file_work_name="монитор-Concat_Prices--May-24--Source.xlsx")
#
#
# #   Заполенение из файла Source
# FileHandler.Fill_Unknown()

# FileHandler = CPN.Consist_Names(category="Ноутбук", #_Source для ноутов для yama заменить Mod_Name_restrict на просто Modification_name
#                                 file_itr="Reports/NB_Pivot_May-24-1.xlsx",
#                                 M='May',
#                                 Y='24',
#                                 file_work_name="ноутбук-Concat_Prices--May-24--Source.xlsx")
#
#
# #   Заполенение из файла Source
# FileHandler.Fill_Unknown()

#FileHandler.Dict_Yama_Names()
#FileHandler.Fill_Yama_Name()


# Заполенение фала Base Stable проверенными
StBase = CPN.Fill_Stable_Base('Ноутбук',
                             'ноутбук-Concat_Prices--May-24--Filled1.xlsx')
StBase.Checked_To_Base()

# # #
# # Заполенение фала Base Stable проверенными
# StBase = CPN.Fill_Stable_Base('Монитор',
#                              'Монитор-Concat_Prices--Mar-23--Filled.xlsx')
# StBase.Checked_To_Base()
# # # #
#Consist_Names_for_mth_report заполняет модели из месячных Pivot
# class Consist_Names_for_mth_report(Consist_Names):
#
#     def __init__(self,
#                  file_itr,
#                   file_work_name="NB_Pivot_classes_Junem--filled-1.xlsx"
#                  work_sheet = "Source"
#                  dir_work="C:\\Users\\User\\Desktop\\Мои документы\\PC\\notebook\\_06\\",
#                  file_itr_page="Models",
#                  itr_model_field="C",
#                  itr_vendor_field="B",
#                   num=1
#                  ):
# #
# MthNB = CPN.Consist_Names_for_mth_report(file_itr="NB_Pivot_Apr-24.xlsx",
#                                         file_work_name="NB_Pivot_unknown_4x-24.xlsx",
#                                         work_sheet="",
#                                         dir_work="C:\\Users\\DSH\\Desktop\\Мои документы\\PC\\notebook\\_04\\",
#                                          num=1
#                                      )
# MthNB.Fill_Models()