import parse_universal_classes as pa

#   main

#def Pagination(self, start=1, finish=-1)

#parse = pa.Parse_CL(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=15).Pagination() #Следить - все ли (для rquest); selenium подрубается со второго запуска
parse = pa.Parse_DNS(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=20).Pagination() #Следить - все ли
#parse = pa.Parse_El(category='ноутбук', scraper='selenium', num_outfile=2 , interrupt=8).Pagination(start=2, finish=101) #Не останавливаться, ставить стопы NB 35 https://www.eldorado.ru/c/noutbuki/

#parse = pa.Parse_CL(category='монитор', scraper='selenium', num_outfile=1, interrupt=5).Pagination() #Следить - все ли
#parse = pa.Parse_DNS(category='монитор', scraper='selenium', num_outfile=1, interrupt=20).Pagination()
#parse = pa.Parse_El(category='монитор', scraper='selenium', num_outfile=1, interrupt=1).Pagination(finish=26) # мониторы 17 https://www.eldorado.ru/c/monitory/


