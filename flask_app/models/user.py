from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = 'rentals'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.role=data['role']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def getAllUsers(cls,data):
        query='SELECT * FROM users'
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            users= []
            for user in users:
                users.append(user)
        return users
        
    @classmethod
    def is_admin(cls, user_id):
        query = "SELECT role FROM users WHERE id = %(user_id)s"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result and result[0]['role'] == 'admin':
            return True
        return False

    @staticmethod
    def validate_user(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invadid email adress!', 'emailRegister')
            is_valid=False
        if len(data['first_name'])<2:
            flash('First name should include more than 2 characters!','firstnameRegister')
            is_valid=False
        if len(data['last_name'])<2:
            flash('Last name should include more than 2 characters!', 'lastnameRegister')
            is_valid=False
        if len(data['password'])<8:
            flash('Password should be at least 8 characters!', 'passwordRegister')
            is_valid=False
        if data['password']!=data['confirmpassword']:
            flash('Passwords should match!','confirmpasswordsRegister')
            is_valid=False
        return is_valid
