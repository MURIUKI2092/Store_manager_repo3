from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import *
from flask_restful import Resource,Api
from ..model.user import  UsersDB

app=Flask(__name__)
api=Api(app,prefix='/api2')
apiBp=Blueprint("api",__name__)


class SingleUser(Resource):
# this method gets a user using his userId
    def get(self,userId):
        U1=UsersDB()
        user=U1.get_single_user(userId)
        if not user:
            message=jsonify(f" The user with the id {userId} was not found")
            return message
        user_got=jsonify({user})
        return user_got        



api.add_resource(SingleUser,"/user")
app.register_blueprint(apiBp)

class AllUsers(Resource):


# this method returns all the users in the database
#first checks the database if there is any user present
# if no user present it returns a message

    def get(self):
        U=UsersDB()
        users=U.get_all_users()
        if not users:

            message=jsonify(f"no users found")
            return  message

        all_users=jsonify({U.get_all_users()})  

        return all_users

api.add_resource(AllUsers,"/users")
app.register_blueprint(apiBp)

class AddUser(Resource):
    def __init__(self,userId,username,email,category,password):

        self.userId=userId
        self.username=username
        self.email=email
        self.category=category
        self.password=password
# this method adds the user account to the database
#it checks if the user is present in the database using the user email
#if present  returns the message the user is present
    def post(self):
        U3=UsersDB()
        user_to_add=U3.add_user(self.username,self.email,self.category,self.password)
        if user_to_add[self.email] in U3:
            return jsonify(f"the user with the email {self.email} already exists")
        user=user_to_add(
            username="username",
            email="email",
            category="category",
            password="password",

        )
        if self.username not in user:
            return f" the field cannot be empty"
        if self.email not in user:
            return f"the email field cannot be empty"
        if self.category not in user:
            return f" the category field cannot be empty"
        if self.password not in user:
            return f"the password field cannot be empty"
        return user



api.add_resource(AddUser,"/users/add")
app.register_blueprint(apiBp)  

class ModifyUser(Resource):
    def __init__(self,userId,username,email,category,password):
        self.userId=userId
        self.username=username
        self.email=email
        self.category=category
        self.password=password
# this method updates user details in the database
#
    def put(self,userId):
        U3=UsersDB()
        user_to_update=U3.get_single_user(userId)
        if not user_to_update:
            message=jsonify(f"the user with the id {userId} is not in the system")
            return message
        resource=request.get_json()
        userName=resource.get("userName")
        email=resource.get("email")
        category=resource.get("category")
        password=resource.get("password")
        user_to_update=U3(userName,email,category,password)

        if userName not in user_to_update:
            message= jsonify("input a username to update")
            return message
        if email not in user_to_update:
            message=jsonify("input user's email to update")
            return message
        if category not in user_to_update:
            message=jsonify("input the category to update")
            return message
        if password not in user_to_update:
            message=jsonify("input the password to update")
            return message
        U3.update_users(userId)
        return user_to_update

# the method deletes the user from the database
    def  delete(self):
        U4=UsersDB()
        user_to_delete=U4.delete_user(self.userId) 
        return user_to_delete       

api.add_resource(ModifyUser,"/user/modify")
app.register_blueprint(apiBp) 