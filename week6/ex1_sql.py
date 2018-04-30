import sqlite3

conn = sqlite3.connect("northwind.db")
conn.text_factory = lambda x: str(x, 'latin1')
query = "SELECT ProductID, ProductName FROM Customers " \
    "NATURAL JOIN Orders NATURAL JOIN \"Order Details\" " \
    "NATURAL JOIN Products WHERE CustomerID = \"ALFKI\""

for product_id, product_name in conn.execute(query):
    print(product_id, product_name)