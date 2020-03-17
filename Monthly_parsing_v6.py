import parse_yama as pynd


parse_link = pynd.Parse_links()
#parse_link.links_to_excel('Ноутбук')
#parse_link.links_to_excel('Монитор')
#parse_link.links_to_excel('Проектор')
#parse_link.links_to_excel('ИБП')

#parse_category = pynd.Parse_models()

#parse_category.prices_to_excel('Cсылки Монитор Feb-20----16--18-37.xlsx')
#parse_category.prices_to_excel('Cсылки ИБП Feb-20----16--19-02.xlsx')
#parse_category.prices_to_excel('Cсылки Проектор Feb-20----16--18-41.xlsx')

parse = pynd.Parse_models_ttx()
#parse = pynd.Parse_models()
#parse.prices_to_excel('Ноутбук', '')
#parse.prices_to_excel('Монитор', 'Cсылки Монитор Mar-20----16--19-13.xlsx')
parse.prices_to_excel('Проектор', 'Cсылки Проектор Mar-20----16--19-23.xlsx')
parse.prices_to_excel('ИБП', 'Cсылки ИБП Mar-20----16--19-17.xlsx ')

#parse_category = pynd.Parse_models()
#parse_category.no_prices_reparse('Ноутбук-Цены-от-Mar-20----17--13-06.xlsx', 'Cсылки Ноутбук Mar-20----16--19-08.xlsx')








