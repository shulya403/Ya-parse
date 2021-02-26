import parse_universal_classes as pa

#   main

#def Pagination(self, start=1, finish=-1)

#parse = pa.Parse_CL(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=15).Pagination() #Следить - все ли (для rquest); selenium подрубается со второго запуска
#parse = pa.Parse_DNS(category='ноутбук', scraper='selenium', num_outfile=1, interrupt=0).Pagination() #цены со скидками!
#parse = pa.Parse_El(category='ноутбук', scraper='requests', num_outfile=1, interrupt=1).Pagination(finish=35) #Не останавливаться, ставить стопы

#parse = pa.Parse_CL(category='монитор', scraper='selenium', num_outfile=2, interrupt=5).Pagination(start=8) #Следить - все ли
parse = pa.Parse_DNS(category='монитор', scraper='selenium', num_outfile=1, interrupt=0).Pagination()
#parse = pa.Parse_El(category='монитор', scraper='requests', num_outfile=1, interrupt=1).Pagination(finish=17)


