from flask.json import jsonify
import psycopg2


class ProductsDB():
    #the constructor
    def __init__(self,productId,category,productName,price):
        self.productId=productId
        self.category=category
        self.ProductName=productName
        self.price=price

#  this method creates a connection to the database
    def connection(self):
        self.connection= psycopg2.connect(
            host="localhost",
            port="5432",
            database="storeproducts",
            user="postgres",
            password="muriuki"
        )

    def executingQueries(self,query,values=None):
        self.query=query
        self.values=values
        cur=self.connection.cursor()
        cur.execute(self,query,self.values)
        self.connection.commit()
        cur.close()

    #closing the connection
    def closingConnection(self):
        self.connection.close()

# the method gets all the products from the database 
    def get_all_products(self):
           #variable for all products
        all_products=ProductsDB.executingQueries("SELECT * FROM product")
#used when there is no product in the database
        if not all_products:
            message=jsonify("There is no product in the database")
            return message
        products=all_products.fetchall()
#iterating through all products
        for p in products:
            return f" {p[0]}  {p[1]}  {p[2]}  {p[3]}"  # returns products as it iterates
        ProductsDB.closingConnection()
# this method returns a single product using the product Id
#searches the product first in the database
#if not found 
    def get_product_by_id(self):
        product=ProductsDB.executingQueries("SELECT * FROM products WHERE id=%s;",(self.productId))
        print("product:",product)

        if not product:
            return None

        current_product=product.fetchone()
        product_needed= current_product(
            productId=current_product[0],
            category=current_product[1],
            productName=current_product[2],
            price=current_product[3]

        )
        ProductsDB.closingConnection()
        return product_needed



    def add_product(self):
        product_to_add=self.executingQueries("INSERT INTO products (id,category,name,price) VALUES (%s,%s,%s,%s);",(self.productId,self.category,self.ProductName,self.price))
        self.closingConnection()
        return product_to_add

    def delete_product(self):
        product_to_delete=ProductsDB.executingQueries("SELECT * FROM products WHERE id=%s;",(self.productId))
        if not product_to_delete:
            message=jsonify(f"The item with the id {self.productId} was not found. check again")
            return message

        product_to_delete=ProductsDB.executingQueries("DELETE FROM products WHERE id=%s;",(self.productId))
        result=jsonify(f"The product has been deleted successfully")
        ProductsDB.closingConnection()
        return result

    def update_product(self):
#it checks whether the product is in the database using the ID       
#this method updates the product in the database using the product id 
# it returns a success message when the item is successfully updated

        product_to_update=ProductsDB.executingQueries("SELECT * FROM products WHERE id=%s;",(self.productId))
        if not  product_to_update:
            message=jsonify(f"The product with the id {self.productId} is not in the store. check your ID again")
            return message
        product_to_update=ProductsDB.executingQueries("UPDATE products SET category=%s ,name=%s ,price=%s WHERE id=%s;",(self.category,self.ProductName,self.price,self.productId))
        result=jsonify(f"the item {self.name} has been  updated successfully ")
        ProductsDB.closingConnection()
        return result
