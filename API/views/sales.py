from flask import Flask,jsonify,Blueprint
from flask_jwt_extended import *
from flask_restful import Resource,Api

from ..model.sales import SalesDB


app=Flask(__name__)
api=Api(app,prefix='/api2')
apiBp=Blueprint("api",__name__)

class SingleSale(Resource):
# this method obtains a single sale using it's ID
    def get(self,saleId):
        S1=SalesDB()
        sale=S1.get_sale_by_ID(saleId)
        if not sale:
            message=jsonify(f"The sale with the Id {saleId} was not found")
            return message
        sale_got=jsonify({sale})
        return sale_got
api.add_resource(SingleSale,"/sale")
app.register_blueprint(apiBp)

class AllSales(Resource):
    def get(self):
        S2=SalesDB()
        sales=S2.get_all_sales()
        if not sales:
            message=jsonify("There are no sales found in the system")
            return message
        all_sales=jsonify({sales})
        return all_sales
api.add_resource(AllSales,"/sales")
app.register_blueprint(apiBp)

class AddSale(Resource):
    def __init__(self,userId,productId,price:float,saleId):
        self.userId=userId
        self.productId=productId
        self.price=price
        self.saleId=saleId
# this method adds a new sale in to the sale table
    def post(self):
        S3=SalesDB()
        sale_to_add=S3.addingSale(self.userId,self.productId,self.price)
        sale=sale_to_add(
            userId="userId",
            productId="productId",
            price="price"

        )
        if self.userId not in sale:
            return f"The userid field cannot be empty"
        if self.productId not in sale:
            return f"The productId field cannot be empty"
        if self.price not in sale:
            return f"the price field cannot be  empty"
        return sale

    def delete(self):
        S4=SalesDB()
        sale_to_delete=S4.delete_sale(self.saleId)
        return sale_to_delete

api.add_resource(AddSale,"/sales/modify")
app.register_blueprint(apiBp)




