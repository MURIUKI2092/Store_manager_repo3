from flask import jsonify
from flask.ext.bcrypt import Bcrypt
import psycopg2

class UsersDB():
    ## the constructor
    def __init__(self,id,name,email,category,password):
        self.id=id
        self.name=name
        self.email=email
        self.category=category
        self.password=password
    #this method creates a connection
    def connection(self):
        self.connection=psycopg2.connect(
            host="localhost",
            port="5432",
            database="storeuser",
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


    def get_all_users(self):
        all_users=self.executingQueries("SELECT * FROM person")
        if not all_users:
            message=jsonify("The database has no users")
            return message
        users= all_users.fetchall()
        return users

    def get_single_user(self):
        user=self.executingQueries('SELECT * FROM person WHERE id=%s;',(self.id))
        print("user: ",user)
        if not user :
            message=jsonify("The user with that id does not exist!")
            return message
        else:
            current_user=user.fetchone()
            user=user(
                id=current_user[0],
                username=current_user[1],
                email=current_user[2],
                category=current_user[3]
            )
            return user

    def add_user(self):
        password=Bcrypt.generate_password_hash(self.password)

        user_to_add=self.executingQueries("INSERT INTO person (name,email,category,password) VALUES (%s,%s,%s,%s);",(self.name,self.email,self.category,password))
        message=jsonify(f"the user {user_to_add[0]} has been added successfully")
        return message

    def delete_user(self):
        user_to_delete=self.executingQueries("SELECT * FROM person WHERE id=%s;",(self.id))
        if not user_to_delete:
            message=jsonify(f"The user with the id {self.id} is not found!")
            return message

        the_user=self.executingQueries("DELETE FROM person WHERE id=%s;",(self.id))
        result=jsonify(f"The user {self.name} has been deleted successfully")
        return result
# verify the user using the email address
    def verify_user(self):
        user_to_verify=self.executingQueries("SELECT password FROM person WHERE email=%s;"(self.email))
        user=user_to_verify.fetchone()

        if not user:
            message=jsonify(f"the user with {self.email} is not found")
            return message
        user_is_valid=check_password_hash(user["password",self.password])
        if user_is_valid is True:
            return f"the user is valid"
        else:
            return f"the user is not valid"

    def update_users(self):
        user_to_update=UsersDB.executingQueries("SELECT * FROM person WHERE id=%s;",(self.id))
        if not  user_to_update:
            message=jsonify(f"The user with the id {self.id} is not in the system. check your ID again")
            return message
        user_to_update=UsersDB.executingQueries("UPDATE person SET name=%s ,category=%s ,email=%s,password=%s WHERE id=%s;",(self.name,self.category,self.email,self.password))
        result=jsonify(f"the user {self.name} has been  updated successfully ")
        UsersDB.closingConnection()
        return result


