import sqlite3

conn = sqlite3.connect("northwind.db")
conn.text_factory = lambda x: str(x, 'latin1')

query = """SELECT OrderID, SUM(UnitPrice*Quantity) 
           FROM Customers NATURAL JOIN ORDERS NATURAL JOIN [Order Details] NATURAL JOIN Products 
           WHERE CustomerID = 'ALFKI' GROUP BY OrderID HAVING SUM(UnitPrice*Quantity) > 500"""


for supid in conn.execute(query):
    print(supid)
