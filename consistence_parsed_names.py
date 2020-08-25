# Модуль сопоставления имен файлов парса
# словарь файлов категорий и прайсов json_consitence
# использует STRAdar
# сопоставить сперва с наименованиями ноутбуков из Pivot
# затем с конфигурациями из ya_ma для соотв модлей
# TODO:
#   Поправить заполнение Ya_UN_Name

import pandas as pd
import os
import json
from pprint import pprint
import numpy as np
import timeit
import time

import StRadar
import math

class Concat_Parse_Files(object):

    def __init__(self,
                 category,
                 M='May',
                 Y=20,
                 JSON_file="cons_parsed_files.json",
                 dir_root="Prices/",
                 dir_work="Handle_base/"):

        self.category = category

        with open(JSON_file, encoding='utf-8') as f:
            self.Files = json.load(f)
    # Структура директорий
        self.dict_dir = self.Files['parsed']
        self.dir_root = dir_root
        self.dir_work = dir_work

    # Месяц
        self.mth = M + "-" + str(Y)

    # Название выходного файла
        self.outfile_name = self.dir_root + \
                   self.dir_work + \
                   self.category + \
                   "-Concat_Prices--" + \
                   self.mth + \
                   "--Source.xlsx"

# Формирователь списка файлов месц.finel.xlsx.category
    def List_Files(self):

        list_files_ = list()
        for dir in self.dict_dir.values():
            if dir == ".":
                dir_ = self.dir_root
            else:
                dir_ = self.dir_root + dir + "/"
            list_files_ += [dir_ + fl for fl in os.listdir(dir_)]

        list_files_to_concat = [fl for fl in list_files_ if
                                ("final.xlsx" in fl.lower())
                                and (self.mth.lower() in fl.lower())
                                and (self.category.lower()) in fl.lower()]


        #for i in list_files_to_concat:
        #    if ("Prices/Ноутбук" in i) and (not "Mod" in i):
        #        list_files_to_concat.remove(i)

        pprint(list_files_to_concat)

        return list_files_to_concat

# Конкатеация
    def Concat_files(self):

        list_files = self.List_Files()

        if list_files:
            df = pd.read_excel(list_files[0], index_col=0)

            if len(list_files) > 1:
                for fl in list_files[1:]:
                    df_ = pd.read_excel(fl, index_col=0)
                    df = pd.concat([df, df_], ignore_index=True)

            df = self.Titled_Vendors(df)
            df = self.Restrict_Ven_Mod_Name(df)

            df.to_excel(self.outfile_name)

# Пусковой Добавление колонки модели без названия вендора
    def Clearing_Mod_Name(self, file_name=""):
        if not file_name:
            file_name = self.outfile_name
        else:
            file_name = self.dir_root + self.dir_work + file_name
        df = pd.read_excel(file_name, index_col=0)

        df = self.Restrict_Ven_Mod_Name(df)

        df.to_excel(file_name[:-5] + "-rest.xlsx")

# Добавление колонки модели без названия вендора
    def Restrict_Ven_Mod_Name(self, df):

        def Restrict_Ven(mod_name):

            list_mod_name = mod_name.split()
            list_mod_name = list_mod_name[1:]

            exit_ = " ".join(list_mod_name)

            return exit_

        df['Modification_name_restrict'] = df['Modification_name'].apply(Restrict_Ven)

        return df


# Пусковой чистка вендоров
    def Clearing_Vendors(self, file_name=""):

        if not file_name:
            file_name = self.outfile_name
        else:
            file_name = self.dir_root + self.dir_work + file_name

        df = pd.read_excel(file_name, index_col=0)
        df = self.Titled_Vendors(df)
        df.to_excel(file_name)

        return df

#   Чистка вендоров
    def Titled_Vendors(self, df):

        for ven in df['Vendor'].unique():
            ven_title = ven.title()
            if ven_title in self.Files["brands"]:
                ven_title = self.Files["brands"][ven_title]

            df['Vendor'].loc[df['Vendor'] == ven] = ven_title

        return df

class Consist_Names(object):

    def __init__(self,
                 category,
                 file_itr,
                 file_itr_page="",
                 itr_model_field="",
                 itr_vendor_field="",
                 JSON_file="cons_parsed_files.json",
                 M='May',
                 Y=20,
                 file_work_name = "",
                 file_base_name = "",
                 dir_root="Prices/",
                 dir_work="Handle_base/",
                 ):


        self.category = category.lower()

        with open(JSON_file, encoding='utf-8') as f:
            self.Files = json.load(f)

        # Месяц
        self.mth = M + "-" + str(Y)

        self.dir_root = dir_root
        self.dir_work = self.dir_root + dir_work

        self.Get_df_base(file_base_name)

        self.Get_df_work(file_work_name)

        self.Get_df_itr(file_itr, file_itr_page, itr_model_field, itr_vendor_field)


        try:
            if self.Files["category"][category]["brands"]:
                self.Corr_Vendor_Name(self.Files["category"][self.category]["brands"])
        except Exception:
            pass

#  Коррекция имен вендоров по словарю category:brands
    def Corr_Vendor_Name(self, dict_names):

        @np.vectorize
        def Change_by_dict(dict_names, ven):

            ven_ = ven.lower()
            if ven_ in list(dict_names.keys()):
                return dict_names[ven_].title()
            else:
                return ven

        self.df_work["Vendor"] = Change_by_dict(dict_names, self.df_work["Vendor"])


#   словарь vendor: модельный ряд
    def Make_Dict_Vendors_Models(self):

        dict_ = dict()
        start_timer = time.time()
        for ven in self.df_itr['Vendor'].unique():
            dict_[str(ven).lower()] = list(self.df_itr[self.df_itr['Vendor'].values == ven]['Name'].values)
        end_timer = time.time()
        print(end_timer - start_timer)

        return dict_

#   df_base
    def Get_df_base(self, file_base_name):

        if file_base_name:
            self.file_base_name = self.dir_work + file_base_name
            self.df_work = pd.read_excel(self.file_base_name, index_col=0)

        else:
            self.file_base_name = self.Get_File_Base()
            if self.file_base_name:
                self.df_base = pd.read_excel(self.file_base_name, index_col=0)

            else:
                self.df_base = pd.DataFrame(columns=['Name',
                                                     'Category',
                                                     'Date',
                                                     'Href',
                                                     'Modification_href',
                                                     'Modification_name',
                                                     'Modification_name_restrict',
                                                     'Ya_UN_Name',
                                                     'Site',
                                                     'Subcategory',
                                                     'Vendor'])
                try:
                    self.file_base_name = self.dir_work + self.Files['category'][self.category]['file_base_name']
                except Exception:
                    print('Нет названия фала базы в JSON для категории: {}'.format(self.category))
                    raise
        print("base:", self.file_base_name)


# Имя файла базы для категории
    def Get_File_Base(self):

        try:
            if self.Files['category'][self.category]['file_base_name'] in os.listdir(self.dir_work):
                return self.dir_work + self.Files['category'][self.category]['file_base_name']
        except Exception:
            pass

        print("Нет базового файла для категории: {}".format(self.category))
        return None

#  df_work
    def Get_df_work(self, file_work_name):
        if file_work_name:
            self.file_work_name = self.dir_work + file_work_name
            self.df_work = pd.read_excel(self.file_work_name, index_col=0)
            #self.df_work.reset_index(inplace=True)
        else:
            self.file_work_name = self.Get_File_Work()
            if self.file_work_name:
                self.df_work = pd.read_excel(self.file_work_name, index_col=0)
                #self.df_work.reset_index(inplace=True)

            else:
                print("Нет рабочиго файла или неверная категория: {}".format(self.category))
                raise
        print("work:", self.file_work_name)

# Имя рабочего файла для категории
    def Get_File_Work(self):

        list_files = os.listdir(self.dir_work)
        for fl in list_files:
            if ("source.xls" in fl.lower()) \
                    and (self.category in fl.lower()) \
                    and ("~" not in fl) \
                    and (self.mth in fl):
                return self.dir_work + fl

        print("Нет базового файла для категории: {}".format(self.category))
        return None

    def Get_df_itr(self, file_itr, file_itr_page, itr_model_field, itr_vendor_field):

        file_itr = self.dir_work + file_itr

        if not itr_model_field:
            itr_model_field = self.Files['category'][self.category]['itr_file']['model_field']

        if not itr_vendor_field:
            itr_vendor_field = self.Files['category'][self.category]['itr_file']['vendor_field']

        if not file_itr_page:
            file_itr_page = self.Files['category'][self.category]['itr_file']['page']

        usecols_ = itr_model_field + "," + itr_vendor_field

        self.df_itr = pd.read_excel(file_itr,
                                    sheet_name=file_itr_page,
                                    names=['Vendor', 'Name'],
                                    usecols=usecols_)

        self.dict_ven_mod = self.Make_Dict_Vendors_Models()
        print("models_list:", file_itr)

    # Отметить уже имеющиеся в базе
    def Fill_Work_by_Base(self):

        self.df_work = self.df_work.apply(self.Сheck_n_Fill_Base_Satble, axis=1)

        print(self.df_work[['Name', 'Modification_name']].loc[self.df_work['Known']])

    def Сheck_n_Fill_Base_Satble(self, row):

        df_work_ = self.df_base[(self.df_base['Site'] == row['Site'])
                        & (self.df_base['Modification_name'] == row['Modification_name'])]
        df_work_.reset_index(inplace=True)

        if not df_work_.empty:
            row['Known'] = True
            row['Name'] = df_work_['Name'].values[0]
            row['Ya_UN_Name'] = df_work_['Ya_UN_Name'].values[0]
        else:
            row['Known'] = False

        return row



# Main (заполенение Name моделей)
    def Fill_Unknown(self):

        if not 'Known' in self.df_work.columns:
            self.Fill_Work_by_Base()

        id_handle = self.df_work[self.df_work['Known'] == False].index

        for id in id_handle:
            mod_name_ = self.df_work.loc[id, 'Modification_name_restrict']
            print(mod_name_)
            try:
                array_vendors_model = self.dict_ven_mod[self.df_work.loc[id, 'Vendor'].lower()]
            except KeyError:
                print("Нет вендора {} в базе".format(self.df_work.loc[id, 'Vendor']))
                array_vendors_model = []

            if array_vendors_model:
                self.df_work.loc[id, 'Name'] = self.Search_ITR_Name(mod_name_, array_vendors_model)


            if self.df_work.loc[id, 'Site'] != 'yama':
                this_name = self.df_work.loc[id, 'Name']
                if this_name:
                    this_name = self.df_work.loc[id, 'Name']
                    if __name__ == '__main__':
                        self.df_work.loc[id, 'Ya_UN_Name'] = self.df_work['Ya_UN_Name'].loc[(self.df_work['Site'] == 'yama')
                                                                                            & (self.df_work['Name'] == this_name)].values[0]
            print(self.df_work.loc[id, ['Name', 'Ya_UN_Name']])

        self.Filled_To_Excel()

#   Взваращает максимум STR из list_search (array_vendors_models)
    def Search_ITR_Name(self, data_, list_search_):

        list_tup_vendor_model = [(key, StRadar.stradar(data_, key, beg_coeff=0.5, bool_restrict=True).result()) for key in
                                 list_search_]
        exit_ = self.Max_list_tup_Name(list_tup_vendor_model)

        return exit_

# Возвращает model с максимальным значением STR
    def Max_list_tup_Name(self, list_tup):

        if list_tup:

            list_tup.sort(key=lambda x: x[1], reverse=True)

            max_STR_coeff = list_tup[0][1]
            max_count = 0
            for i in list_tup:
                if i[1] < max_STR_coeff:
                    break
                else:
                    max_count += 1

            if max_count > 1:
                list_max_coeff_names = [(m, len(list_tup[m][0])) for m in range(max_count)]
                list_max_coeff_names.sort(key=lambda x: x[1])

                return list_tup[list_max_coeff_names[0][0]][0]

            return list_tup[0][0]

        else:
            return None

# Формирует self.dict_yama_names
    def Dict_Yama_Names(self):

        @np.vectorize
        def Clear_Vendor_Name(str_, ven):
             return str_.replace(ven+" ", "")

        dict_ = dict()

        array_yama_vendors = self.df_work[self.df_work['Site'] == 'yama']['Vendor'].unique()

        for ven in array_yama_vendors:

            ser_ = self.df_work[(self.df_work['Site'] == 'yama')
                                               & (self.df_work['Vendor'] == ven)]['Modification_name']
            #for i, ser in ser_.items():
            #print(ser_)
            ser_ = Clear_Vendor_Name(ser_, ven)

            dict_[ven.lower()] = list(ser_)

        self.dict_yama_names = dict_

    def Search_Yama_Name(self, row_):

        if row_['Site'] != 'yama':
            vendor_ = row_['Vendor']
            try:
                list_yama_names = self.dict_yama_names[vendor_.lower()]
            except KeyError:
                print("Нет вендора у yama:", vendor_)
                list_yama_names = []

            search_ = row_['Modification_name'].replace(vendor_, "")
            print(search_)
            list_tup_yama = [(key, StRadar.stradar(key, search_, beg_coeff=0.5, bool_restrict=True).result()) for key
                             in list_yama_names]

            exit_ = self.Max_list_tup_Name(list_tup_yama)
            print(row_['index'], row_['Site'], vendor_, search_, "--", exit_)
        else:
            return row_['Modification_name']

        return exit_

    def Fill_Yama_Name(self):

        for iter, row in self.df_work.iterrows():
            if row['Ok'] == 0:
                self.df_work.loc[iter, 'Yama_name'] = self.Search_Yama_Name(row)

        #self.df_work[self.df_work['Ok'] == 0]['Yama_name'] = self.df_work[self.df_work['Ok'] == 0].apply(self.Search_Yama_Name, axis=1)

        self.df_work.to_excel(self.file_work_name.replace('.xlsx', '_yama.xlsx'))

#записываем обработанный df_work в файл
    def Filled_To_Excel(self):

        file_name_ = self.file_work_name.replace('Source', 'Filled')
        self.df_work.to_excel(file_name_)

#   Заливка обновленных данных в базу
class Fill_Stable_Base(Consist_Names):

    def __init__(self,
                 category,
                 cheked_file_name,
                 file_base_name="",
                 JSON_file="cons_parsed_files.json",
                 dir_root="Prices/",
                 dir_work="Handle_base/"
                 ):

        self.category = category.lower()

        with open(JSON_file, encoding='utf-8') as f:
            self.Files = json.load(f)

        self.dir_root = dir_root
        self.dir_work = self.dir_root + dir_work


        self.cheked_file_name = self.dir_work + cheked_file_name

        self.Get_df_base(file_base_name)

    def Get_df_Checked(self):
        df_ = pd.read_excel(self.cheked_file_name, index_col=0)
        df_ = df_[df_['Known'] == False]
        for i in df_.columns:
            if 'ok' in i.lower():
                df_ = df_[df_[i] == 1]

        df_.drop_duplicates(subset=['Modification_name', 'Site'], inplace=True)

        return df_

    def Make_buckup_Stable_base(self):

        file_backup_name = self.dir_work + 'backup_' + time.strftime('%d-%m-%y--%H-%M', time.gmtime(
            time.time())) + "_" + self.category + "_Stable.xlsx"
        self.df_base.to_excel(file_backup_name)


    def Checked_To_Base(self):

        df_ = self.Get_df_Checked()

        self.Make_buckup_Stable_base()

        set_col_base_ = set(self.df_base.columns)
        self.df_base = pd.concat([self.df_base, df_], ignore_index=True)
        self.df_base.drop_duplicates(subset=['Modification_name', 'Site'], keep='last', inplace=True)

        set_col_concat = set(self.df_base.columns)
        set_to_drop = set_col_concat - set_col_base_
        self.df_base.drop(columns=list(set_to_drop), inplace=True)

        self.df_base.to_excel(self.file_base_name)

class Consist_Names_for_mth_report(Consist_Names):

    def __init__(self,
                    file_itr,
                    file_work_name="",
                    work_sheet="Source",
                    dir_work="C:\\Users\\User\\Desktop\\Мои документы\\PC\\notebook\\_07\\",
                    file_itr_page = "Models",
                    itr_model_field = "C",
                    itr_vendor_field = "B",
                    num=1
                    ):
        if not file_work_name:
            file_work_name = file_itr

        self.dir_work = dir_work
        self.file_out = self.dir_work + file_work_name.replace(".xls","").replace("--filled", "") + "--filled" + "-" + str(num) + ".xlsx"
        print(self.file_out)

        self.Get_df_work(file_work_name, work_sheet)

        self.Get_df_itr(file_itr, file_itr_page, itr_model_field, itr_vendor_field)

        print(self.df_work.head())
        print(self.df_itr.head())


        #  df_work
    def Get_df_work(self, file_work_name, work_sheet):
            if file_work_name:
                self.file_work_name = self.dir_work + file_work_name
                if work_sheet:
                    self.df_work = pd.read_excel(self.file_work_name, sheet_name=work_sheet)
                else:
                    self.df_work = pd.read_excel(self.file_work_name)

            else:
                print("Неизвестное имя файла file_work_name")
                raise

            print("work:", self.file_work_name)

#   словарь vendor: модельный ряд
#     def Make_Dict_Vendors_Models(self):
#
#         dict_ = dict()
#         start_timer = time.time()
#         for ven in self.df_itr['Vendor'].unique():
#             dict_[str(ven).lower()] = list(self.df_itr[self.df_itr['Vendor'].values == ven]['Name'].values)
#         end_timer = time.time()
#         print(end_timer - start_timer)
#
#         return dict_

# Main (заполенение Name моделей)
    def Fill_Models(self):

        id_handle = self.df_work[self.df_work['Model'].isna()].index
        self.Corr_Vendor_Name()

        for id in id_handle:
            mod_name_ = self.df_work.loc[id, 'Source']
            print(mod_name_)
            try:
                array_vendors_model = self.dict_ven_mod[self.df_work.loc[id, 'Brand'].lower()]
            except KeyError:
                print("Нет вендора {} в базе".format(self.df_work.loc[id, 'Brand']))
                array_vendors_model = []

            if array_vendors_model:
                self.df_work.loc[id, 'Model'] = self.Search_ITR_Name(mod_name_, array_vendors_model)


            print(self.df_work.loc[id, ['Source', 'Model']])

        self.Filled_To_Excel()

        #  Коррекция имен вендоров по словарю category:brands

    def Corr_Vendor_Name(self):

            print(self.df_work['Brand'].values)
            print(self.df_work['Brand'].to_list())


            self.df_work['Brand'] = self.df_work['Brand'].apply(lambda x: str(x).title().replace(" ", ""))


    def Filled_To_Excel(self):

        self.df_work.to_excel(self.file_out)



















