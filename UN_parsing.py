import parse_universal_classes as pa

#main

#parse = pa.Parse_CL(category='ноутбук', scraper='requests', num_outfile=3, interrupt=15).Pagination(33, 56)
#parse = pa.Parse_DNS(category='ноутбук', scraper='requests', num_outfile=2, interrupt=1).Pagination(start=2)
parse = pa.Parse_El(category='ноутбук', scraper='requests', num_outfile=1, interrupt=1).Pagination()
