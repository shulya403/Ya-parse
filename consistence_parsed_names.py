# Модуль сопоставления имен файлов парса
# словарь файлов категорий и прайсов json_consitence
# использует STRAdar
# сопоставить сперва с наименованиями ноутбуков из Pivot
# затем с конфигурациями из ya_ma для соотв модлей
# TODO:
#   проверить руками
#   прибить лист с TTX - Yandex
#   сделать сводную

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


        for i in list_files_to_concat:
            if ("Prices/Ноутбук" in i) and (not "Mod" in i):
                list_files_to_concat.remove(i)

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

            outfile_name = self.dir_root + \
                           self.dir_work + \
                           self.category + \
                           "-Concat_Prices--" + \
                           self.mth + \
                           "--Source.xlsx"

            df.to_excel(outfile_name)

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


        # Структура директорий
        self.dict_dir = self.Files['parsed']

        # Месяц
        self.mth = M + "-" + str(Y)
        self.dir_root = dir_root
        self.dir_work = self.dir_root + dir_work

        if file_work_name:
            self.file_work_name = self.dir_work + file_work_name
            self.df_work = pd.read_excel(self.file_work_name, index_col=0)
            self.df_work.reset_index(inplace=True)
        else:
            self.file_work_name = self.Get_File_Work()
            if self.file_work_name:
                self.df_work = pd.read_excel(self.file_work_name, index_col=0)

            else:
                print("Нет рабочиго файла или неверная категория: {}".format(self.category))
                raise
        print("work:", self.file_work_name)

        if file_base_name:
            self.file_base_name = self.dir_work + file_base_name
            self.df_work = pd.read_excel(self.file_base_name, index_col=0)

        else:
            self.file_base_name = self.Get_File_Base()
            if self.file_base_name:
                self.df_base = pd.read_excel(self.file_base_name, index_col=0)

            else:
                self.df_base = pd.DataFrame(columns=['Name',
                                                     'Yama_name',
                                                     'Category',
                                                     'Date',
                                                     'Href',
                                                     'Modification_href',
                                                     'Modification_name',
                                                     'Modification_price',
                                                     'Ya_UN_Name',
                                                     'Quantity',
                                                     'Site',
                                                     'Subcategory',
                                                     'Vendor'])
                try:
                    self.file_base_name = self.dir_work + self.Files['category'][self.category]['file_base_name']
                except Exception:
                    print('Нет названия фала базы в JSON для категории: {}'.format(self.category))
                    raise
        print("base:", self.file_base_name)


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
                                    names=['Vendor','Name'],
                                    usecols=usecols_)

        self.dict_ven_mod = self.Make_Dict_Vendors_Models()
        print("models_list:", file_itr)

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


#словарь vendor: модельный ряд
    def Make_Dict_Vendors_Models(self):

        dict_ = dict()
        start_timer = time.time()
        for ven in self.df_itr['Vendor'].unique():
            dict_[ven.lower()] = list(self.df_itr[self.df_itr['Vendor'].values == ven]['Name'].values)
        end_timer = time.time()
        print(end_timer - start_timer)

        return dict_

# Имя файла базы для категории
    def Get_File_Base(self):

        try:
            if self.Files['category'][self.category]['file_base_name'] in os.listdir(self.dir_work):
                return self.dir_work + self.Files['category'][self.category]['file_base_name']
        except Exception:
            pass

        #list_files = os.listdir(self.dir_work)
        #for fl in list_files:
        #    if ("stable.xls" in fl.lower()) \
        #            and (self.category in fl.lower()) \
        #            and ("~" not in fl):
        #        return self.dir_work + fl

        print("Нет базового файла для категории: {}".format(self.category))
        return None

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

    def Lower_DF(self, df):

        for col in df.columns:
            df[col] = df[col].str.lower()

# Отметить уже имеющиеся в базе
    def Fill_Work_by_Base(self):

        @np.vectorize
        def Check_Known(self, mname, site, id):

            if mname in self.df_base[self.df_base['Site'].values == site]['Modification_name'].values:

                this_ = self.df_base[self.df_base['Modification_name'] == mname]
                self.df_work.loc[id, 'Name'] = this_['Name'].values[0]
                self.df_work.loc[id, 'Yama_name'] = this_['Yama_name'].values[0]

                return True
            else:
                return False

        #self.Lower_DF(self.df_base
        self.df_work['Known'] = Check_Known(self, self.df_work['Modification_name'], self.df_work['Site'], self.df_work.index)

# Main (заполенение моделей)
    def Fill_Unknown(self):

        if not 'Known' in self.df_work.columns:
            self.Fill_Work_by_Base()

        id_handle = self.df_work[self.df_work['Known'] == False].index

        for id in id_handle:
            mod_name_ = self.df_work.loc[id, 'Modification_name'].\
                replace(self.df_work.loc[id, 'Vendor'], "")
            print(mod_name_)
            try:
                array_vendors_model = self.dict_ven_mod[self.df_work.loc[id, 'Vendor'].lower()]
            except KeyError:
                print("Нет вендора {} в базе".format(self.df_work.loc[id, 'Vendor']))
                array_vendors_model = []

            if array_vendors_model:
                list_tup_vendor_model = [(key, StRadar.stradar(mod_name_, key, beg_coeff=0.5).result()) for key in array_vendors_model]
                list_tup_vendor_model.sort(key=lambda x: x[1], reverse=True)

                self.df_work.loc[id, 'Name'] = list_tup_vendor_model[0][0]
                print(self.df_work.loc[id, 'Name'])

        self.Filled_To_Excel()


#записываем обработанный df_work в файл
    def Filled_To_Excel(self):

        file_name_ = self.file_work_name.replace('Source', 'Filled')
        self.df_work.to_excel(file_name_)

#Заливка обновленных данных в базу

    def Checked_To_Base(self, category, cheked_file_name):

        cheked_file_name = self.dir_work + cheked_file_name
        df_ = pd.read_excel(cheked_file_name, index_col=0)
        df_ = df_[df_['Known'] == False]
        df_.drop(columns=['Known'])

        #if mth:
        #    df_['Date_add'] = mth
        #else:
        #    df_['Date_add'] = self.mth

        set_col_base_ = set(self.df_base.columns)
        self.df_base = pd.concat([self.df_base, df_], ignore_index=True)
        set_col_concat = set(self.df_base.columns)
        set_to_drop = set_col_concat - set_col_base_
        self.df_base.drop(columns=list(set_to_drop))

        self.df_base.to_excel(self.file_base_name)























