import sqlite3

conn = sqlite3.connect("northwind.db")
conn.text_factory = lambda x: str(x, 'latin1')

query = "SELECT count(*) FROM (SELECT SupplierID FROM Products NATURAL JOIN Suppliers GROUP BY SupplierID HAVING count(DISTINCT CategoryID) BETWEEN 2 AND 4)"

# print("OrderID\t ProductID\t CategoryID\t ProductName")
# print(conn.execute(query).fetchone())
# for supid, company, product_id, product_name, category_id in conn.execute(query):
#     print(supid, '\t\t', company.encode(),  category_id, '\t\t', product_name.encode())
for supid in conn.execute(query):
    print(supid)
