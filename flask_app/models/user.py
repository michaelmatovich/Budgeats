from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    schema_name = "budgeats_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.bands_joined = []

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"

        result = connectToMySQL(cls.schema_name).query_db(query, data)

        return result
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        return cls(result[0])

    @classmethod
    def does_exist(cls,data):
        does_exist = True

        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        if not result:
            does_exist = False

        return does_exist

    @classmethod
    def user_does_exist(cls,data):
        does_exist = True

        query = "SELECT * FROM users WHERE username = %(username)s;"

        result = connectToMySQL(cls.schema_name).query_db(query,data)

        if not result:
            does_exist = False

        return does_exist

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data["username"]) < 3:
            flash("Username must be at least 3 characters long.")
            is_valid = False
        if len(data["email"]) < 1:
            flash("Email address must be present.")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Please enter a valid email address.")
            is_valid = False
        if User.does_exist({"email": data["email"]}) == True:
            flash("This email address is already registered.")
            is_valid = False
        if User.user_does_exist({"username": data["username"]}):
            flash("This username is already registered.")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Password must match Confirmation Password.")   
            is_valid = False
        return is_valid




