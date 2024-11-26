import parse_universal_classes as pa

#   main

#def Pagination(self, start=1, finish=-1)

# Nov-24 parse = pa.Parse_CL(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=15).Pagination(start=13) #Следить - все ли (для rquest); selenium подрубается со второго запуска
# Nov-24 parse = pa.Parse_DNS(category='ноутбук', scraper='selenium', num_outfile=2, interrupt=5).Pagination(start=25) #Следить - все ли
#parse = pa.Parse_El(category='ноутбук', scraper='selenium', num_outfile=2 , interrupt=8).Pagination(start=2, finish=101) #Не останавливаться, ставить стопы NB 35 https://www.eldorado.ru/c/noutbuki/
#parse = pa.Parse_OZ(category='ноутбук', scraper='selenium', num_outfile=0, interrupt=5).Pagination()
#parse = pa.Parse_Ya(category='ноутбук', scraper='selenium', num_outfile=0, interrupt=0, user_id=1).\
#Pagination(vendors=[])
# "data-auto": "snippet-price-old"
# "data-auto": "price-value"
# Nb ["Acer", "Alienware", "Apple", "Acer", "Apple", "Asus", "Dell", "Honor", "HP", "Huawei", "Lenovo", "MSI"]
#"class": "_24Evj"

# Oct-24 parse = pa.Parse_CL(category='монитор', scraper='selenium', num_outfile=0, interrupt=15).Pagination() #Следить - все ли
# Nov-24 parse = pa.Parse_DNS(category='монитор', scraper='selenium', num_outfile=1, interrupt=5).Pagination(start=18)
#parse = pa.Parse_El(category='монитор', scraper='selenium', num_outfile=1, interrupt=1).Pagination(finish=26) # мониторы 17 https://www.eldorado.ru/c/monitory/
# parse = pa.Parse_OZ(category='монитор', scraper='selenium', num_outfile=0, interrupt=5).Pagination()
# Aug-24 parse = pa.Parse_Ya(category='монитор', scraper='selenium', num_outfile=0, interrupt=2, user_id=1).\
#     Pagination(vendors=[])



# Mnt ["Acer","AOC", "Asus", "BenQ", "Dell", "HP", "Iiyama", "LG", "Philips", "Samsung", "Viewsonic", "Lenovo", "MSI", "NEC", "Xiaomi", "Gigabyte", "Huawei",
#  "DEXP", "Ardor Gaming","Titan Army", "Digma","SunWind","Thunderobot","NPC","Chiq","Exegate","Sanc","Lime","Valday","Hiper","Raskat",
#  "Irbis","Cooler Master","Pinebro","Cbr","Hisense","Mucai","GMNG","HKC","RDW","Classic Solution","Leff","Machenke","Eizo","ACD","Dahua","Tesla", "Azerty"]

#parse = pa.Parse_Ya(category='проектор', scraper='selenium', num_outfile=0, interrupt=5, user_id=1).\
#   Pagination(vendors=[])
#parse = pa.Parse_DNS(category='проектор', scraper='selenium', num_outfile=1, interrupt=5).Pagination(start=4)
# Prj ['Acer', 'BenQ', 'Epson', 'Infocus', 'LG', 'NEC', 'Optoma', 'Sony', 'Viewsonic', 'Xiaomi', 'Barco', 'Canon', 'Casio', 'Christie', 'Hiper', 'Hitachi', 'JVC', 'Panasonic', 'Ricoh', 'Smart', 'Vivitek']

# parse = pa.Parse_Ya(category='ибп', scraper='selenium', num_outfile=1, interrupt=1).Pagination(vendors=['APC'])
# Ups 'vendors': ['APC','Eaton','Ippon','Delta','Cyberpower','Powercom','Vertiv','SI','Huawei','Powerman','Impuls','Eltena-Inelt','Legrand','Socomec','Riello','Maklesan',
#             'GE','DKC','Tripp Lite','AEG','Irbis','Sven','Hiper']

#parse = pa.Parse_Ya(category='logitech', scraper='selenium', num_outfile=0, interrupt=1).Pagination(vendors=[])
#parse = pa.Parse_DNS(category='ибп', scraper='selenium', num_outfile=0, interrupt=5).Pagination()