from query import generate_query
decoded_mql='"stfu stfu" in ("Google", "VMware") AND "Creation Date" < "11mm" AND downloads > abc order by "Creation Date" DESC'
mysql_query=generate_query(decoded_mql)
print(mysql_query)
