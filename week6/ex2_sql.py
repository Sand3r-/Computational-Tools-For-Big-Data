import sqlite3

conn = sqlite3.connect("northwind.db")
conn.text_factory = lambda x: str(x, 'latin1')
query = "SELECT OrderID, ProductID, ProductName, CategoryID FROM Customers " \
    "NATURAL JOIN Orders NATURAL JOIN \"Order Details\" " \
    "NATURAL JOIN Products WHERE CustomerID = \"ALFKI\" AND OrderID IN (" \
        "SELECT OrderID FROM Orders NATURAL JOIN Customers c " \
        "NATURAL JOIN \"Order Details\" NATURAL JOIN Products p " \
        "WHERE c.CustomerID LIKE \"ALFKI\" "\
        "GROUP BY OrderID HAVING max(p.CategoryID) != min(p.CategoryID)" \
    ")"

print("OrderID\t ProductID\t CategoryID\t ProductName")
for order_id, product_id, product_name, category_id in conn.execute(query):
    print(order_id, '\t', product_id, '\t\t', category_id, '\t\t', product_name)
