from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Del_Headset:
    db_name = DB_NAME

    def __init__(self, data):
        self.serial_number = data['serial_number']
        self.operator = data['operator']
        self.statusi = data['statusi']
        self.user_id = data['user_id']
        self.serial_number = data['serial_number']
    
    
    @classmethod
    def get_all_del_headsets(cls):
        query = """
            SELECT 
                del_headsets.*, 
                users.username AS it_name
            FROM del_headsets
            LEFT JOIN users ON del_headsets.user_id = users.user_id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        headsets = []
        if results:
            for headset in results:
                headsets.append(headset)
        return headsets
    
    
    @classmethod
    def headset_returnd(cls, data):
        query = """
            UPDATE del_headsets
            SET
                statusi = 1
            WHERE serial_number = %(serial_number)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def add_del_headset(cls, data):
        query = """
            INSERT INTO del_headsets (
                serial_number,
                operator,
                user_id
            ) VALUES (
                %(serial_number)s,
                %(operator)s,
                %(user_id)s
            );
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def upload_del_headset(cls, data):
        query = """
            INSERT INTO del_headsets (
                serial_number,
                operator,
                statusi,
                user_id
            ) VALUES (
                %(serial_number)s,
                %(operator)s,
                %(statusi)s,
                %(user_id)s
            );
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_headset(data):
        is_valid = True
        if len(data['serial_number']) < 1:
            flash("Headset SN is required", "del_add")
            is_valid = False
        if len(data['operator']) < 1:
            flash("Operator is required", "del_add")
            is_valid = False
        return is_valid
        