from query import generate_query
decoded_mql='"creator" in ("Google", "VMware") order by "Creation Date" DESC'
mysql_query=generate_query(decoded_mql)
print(mysql_query)
