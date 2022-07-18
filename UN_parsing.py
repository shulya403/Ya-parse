import parse_universal_classes as pa

#   main

#def Pagination(self, start=1, finish=-1)

#parse = pa.Parse_CL(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=15).Pagination() #Следить - все ли (для rquest); selenium подрубается со второго запуска
parse = pa.Parse_DNS(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=5).Pagination() #Следить - все ли
#parse = pa.Parse_El(category='ноутбук', scraper='selenium', num_outfile=2 , interrupt=8).Pagination(start=2, finish=101) #Не останавливаться, ставить стопы NB 35 https://www.eldorado.ru/c/noutbuki/
#parse = pa.Parse_Ya(category='ноутбук', scraper='selenium', num_outfile=0, interrupt=1, user_id=1).Pagination(vendors=[])

# Nb ["Acer", "Alienware", "Apple", "Asus", "Dell", "Honor", "HP", "Lenovo", "MSI", "Huawei"]

#parse = pa.Parse_CL(category='монитор', scraper='selenium', num_outfile=1, interrupt=5).Pagination() #Следить - все ли
#parse = pa.Parse_DNS(category='монитор', scraper='selenium', num_outfile=0, interrupt=20).Pagination()
#parse = pa.Parse_El(category='монитор', scraper='selenium', num_outfile=1, interrupt=1).Pagination(finish=26) # мониторы 17 https://www.eldorado.ru/c/monitory/
#parse = pa.Parse_Ya(category='монитор', scraper='selenium', num_outfile=1, interrupt=1, user_id=1).Pagination(vendors=["HP", "Iiyama", "LG", "Philips", "Samsung", "Viewsonic", "Lenovo", "MSI", "NEC", "Xiaomi", "Gigabyte"])

# Mnt ["Acer","AOC", "Asus", "BenQ", "Dell", "HP", "Iiyama", "LG", "Philips", "Samsung", "Viewsonic", "Lenovo", "MSI", "NEC", "Xiaomi", "Gigabyte"]

#parse = pa.Parse_Ya(category='проектор', scraper='selenium', num_outfile=1, interrupt=1, user_id=1).Pagination(vendors=['JVC','Panasonic', 'Ricoh','Smart','Vivitek'])
# Prj ['Acer','BenQ','Epson','Infocus','LG','NEC','Optoma','Sony','Viewsonic','Xiaomi','Barco','Canon','Casio','Christie','Hiper ','Hitachi','JVC','Panasonic',
#             'Ricoh','Smart','Vivitek']

#parse = pa.Parse_Ya(category='ибп', scraper='selenium', num_outfile=1, interrupt=1).Pagination(vendors=['Hiper'])
# Ups 'vendors': ['APC','Eaton','Ippon','Delta','Cyberpower','Powercom','Vertiv','SI','Huawei','Powerman','Impuls','Eltena-Inelt','Legrand','Socomec','Riello','Maklesan',
#             'GE','DKC','Tripp Lite','AEG','Irbis','Sven','Hiper']
