from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import *
from flask_restful import Resource,Api
from API. import ProductsDB

app=Flask(__name__)
api=Api(app,prefix='/api2')
apiBp=Blueprint("api",__name__)

class AllProducts(Resource):
#this method returns all products in the database
    def get(self):
        P=ProductsDB()
        products=P.get_all_products()
        if not products:
            message=jsonify("There are no products found")
            return message
        result=jsonify({products })
        return result


api.add_resource(AllProducts,"/products")
app.register_blueprint(apiBp)
class SingleProduct(Resource):
      # @jwt_required
   #this method returns a single product from  the database using a key productId

    def get(self,productId):
        P1=ProductsDB
        product=P1.get_product_by_id(productId)
        if not product:
            message=jsonify(f"The item with id {productId} is not found")
            return message

        result=jsonify({P1.get_product_by_id(productId)})
        return result

api.add_resource(SingleProduct,"/product")
app.register_blueprint(apiBp)

class AddProduct(Resource):

    def __init__(self, productId,category,productname,price):
        self.productId=productId
        self.category=category
        self.productname=productname
        self.price=price

    def post(self):
        P2=ProductsDB()
        product_to_add=P2.add_product(self.category,self.productname,self.price)

        product=product_to_add(
            category="category",
            name="productName",
            price="price"
                )
        if self.category not in product:
            message=jsonify("the field cannot be empty")
            return message
        elif self.productname not in product:
            message=jsonify("The name field cannot be empty")
            return message
        elif self.price not in product:

            message=jsonify("The price field cannot be  empty")
            return message

        return  product

api.add_resource(AddProduct,"/addproduct")
app.register_blueprint(apiBp)                       
class ModifyProduct(Resource):
    def __init__(self, productId,category,productname,price):
        self.productId=productId
        self.category=category
        self.productname=productname
        self.price=price
#it checks whether the product is in the database using the ID       
#this method updates the product in the database using the product id 
# it returns a success message when the item is successfully updated
    def put(self,productId):
        P3=ProductsDB()
        product_to_update=P3.get_product_by_id(productId)
        if not product_to_update:
            message=jsonify("The product is not found in the system. check again!")
            return message

        resource=request.get_json()

        category=resource.get("category")
        productName=resource.get("name")
        price=resource.get("price") 


        product_to_update=P3(category,productName,price)

        if category not in product_to_update:
            message= jsonify("Input the category field to update")
            return message
        if productName not in product_to_update:
            message=jsonify("input the product name to update") 
            return message
        if price not in product_to_update:
            message=jsonify("input the price value to update")

        P3.update_product(productId)
        return product_to_update


#This method deletes a single product using its ID

    def delete(self,productId):
        P4=ProductsDB()
        product_to_delete=P4.delete_product(productId)
        return product_to_delete


api.add_resource(ModifyProduct,"/product/modify")
app.register_blueprint(apiBp)  