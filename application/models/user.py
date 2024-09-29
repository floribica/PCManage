from flask_bcrypt import Bcrypt

from flask import flash, request

from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL
from application.helpers.email_check import check_email


DB_NAME = load_db()


class User:
    db_name = DB_NAME

    def __init__(self, data):

        self.user_id = data['user_id']
        self.username = data['username']
        self.password = data['password']
        self.role = data['role']
        self.email = data['email']
    
    
    @classmethod
    def get_user_by_username(cls, data):
        query = """
            SELECT
                *
            FROM users
            WHERE username = %(username)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        
        
    @classmethod
    def create_user(cls, data):
        query = """
            INSERT INTO users
                (username, password, role, email)
            VALUES
                (%(username)s, %(password)s, %(role)s, %(email)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def get_by_username(cls, data):
        query = """
            SELECT
                *
            FROM users
            WHERE username = %(username)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return True
        return False
    
    
    @classmethod
    def update_password(cls, data):
        query = """
            UPDATE users
            SET
                password = %(password)s
            WHERE username = %(username)s
            AND email = %(email)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def user_reser_password(cls, data):
        query = """
            UPDATE users
            SET
                password = %(password)s
            WHERE username = %(username)s
        """
        connectToMySQL(cls.db_name).query_db(query, data)
        
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['username']) < 2:
            flash("Username must be at least 2 characters.", "register")
            is_valid = False
        if not check_email(data['email']):
            flash("Invalid email address", "register")
            return False
        if data["role"] not in ["admin", "it", "recruiter","receptionist"]:
            flash("Invalid role.", "register")
            is_valid = False
        return is_valid
    
    
    @staticmethod
    def validate_reset(data):
        is_valid = True
        if not User.get_by_username(data):
            flash("Invalid username or email.", "reset")
            is_valid = False
        if len(data['username']) < 2:
            flash("Username must be at least 2 characters.", "reset")
            is_valid = False
        if not check_email(data['email']):
            flash("Invalid email address", "reset")
            return False
        return is_valid
    
    
    @staticmethod
    def validate_user_reset(data):
        is_valid = True
        if len(data['username']) < 2:
            flash("Username must be at least 2 characters.", "reset")
            is_valid = False
        user = User.get_user_by_username(data)
        if not Bcrypt().check_password_hash(user['password'], data['old_password']):
            flash("Invalid password.", "reset")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match.", "reset")
            is_valid = False
        return is_valid
    