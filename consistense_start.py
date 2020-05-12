import consistence_parsed_names as CPN

#May = CPN.Concat_Parse_Files('Ноутбук')
#May.Concat_files()

FileHandler = CPN.Consist_Names("Ноутбук", "NB_Pivot_Mar (Восстановленный).xlsm")
#FileHandler.Fill_Work_by_Base()

#   Заполенение из файла Source
FileHandler.Fill_Unknown()

#   Заполенение фала Base Stable проверенными
#FileHandler.Checked_To_Base('Ноутбук', 'Ноутбук-Concat_Prices--May-20--Checked.xlsx')