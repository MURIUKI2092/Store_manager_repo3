import psycopg2
from  model.products import ProductsDB
from model.user import UsersDB

class SalesDB(UsersDB,ProductsDB):
    def __init__(self,saleId,):
        self.saleId=saleId
        self.id
        self.productId

    #this method creates a connection
    def connection(self):
        self.connection=psycopg2.connect(
            host="localhost",
            port="5432",
            database="storesales",
            user="postgres",
            password="muriuki"
        )
    #this method deals with  execution of queries,creates a cursor and also closes it
    def executingQueries(self,query,values=None):
        self.query=query
        self.values=values
        cur=self.connection.cursor()
        cur.execute(self.query,self.values)
        self.connection.commit()
        cur.close()
#This method closes the connection
    def closingConnection(self):
        self.connection.close()

# the method adds a sale in to the database
    def addingSale(self):
        sale_to_add=self.executingQueries("INSERT INTO sale (id,userId,productId,price) VALUES (%s,%s,%s,%s);",(self.saleId,self.id,self.productId,self.price))
        self.closingConnection()
        return sale_to_add
# the method deletes a sale from the database 
# it uses the salesid to obtain the object to delete  
    def delete_sale(self):
        sale_to_delete=SalesDB.executingQueries("SELECT * FROM sale WHERE id=%s;",(self.saleId))
        if not sale_to_delete:
            message=jsonify(f"The item with the id {self.saleId} does not exist")
            return message
        sale_to_delete=SalesDB.executingQueries("DELETE FROM sale WHERE id=%s;",(self.saleId))
        to_display=jsonify("The sale has been deleted successfully")
        self.closingConnection()
        return to_display
# the method gets all the sales in the database
# if no sale present a message is relayed
    def get_all_sales(self):
        all_sales=SalesDB.executingQueries("SELECT * FROM sale")
        if not all_sales:
            message=jsonify("There are no sale in the database")
            return message
        sales=all_sales.fetchall()
        for s in sales:
            return f"{s[0]} {s[1]}  {s[2]}  {s[3]}"
        self.closingConnection()
#this method gets a single sale using it's Id
# if the sale is not found a message is relayed
    def get_sale_by_ID(self):
        sale=SalesDB.executingQueries("SELECT * FROM sale WHERE id=%s;",(self.saleId))
        if not sale:
            message=jsonify(f"the sale with id {self.saleId} does not exist. check again")
            return message
        the_sale=sale.fetchone()
        self.closingConnection()
        return  the_sale

s=SalesDB() 