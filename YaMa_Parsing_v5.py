import parse_yama as pyama

    #Вызов
Data = pyama.Parse()
#links.links_to_excel('Ноутбук')
#links.links_to_excel('Монитор')
#links.links_to_excel('Проектор')
#links.links_to_excel('ИБП')

link_file = 'Cсылки Монитор Jan-20----18--18-36.xlsx'
Data.prices_to_excel(link_file)



