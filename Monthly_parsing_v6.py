import parse_yama as pynd


#parse_link = pynd.Parse_links()
#parse_link.links_to_excel('Ноутбук')
#parse_link.links_to_excel('Монитор')
#parse_link.links_to_excel('Проектор')
#parse_link.links_to_excel('ИБП')

parse_category = pynd.Parse_models()

parse_category.prices_to_excel('Cсылки Ноутбук Feb-20----16--18-29.xlsx')


