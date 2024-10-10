from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Headset:
    db_name = DB_NAME

    def __init__(self, data):
        self.headset_id = data['headset_id']
        self.adapter_model = data['adapter_model']
        self.adapter_sn = data['adapter_sn']
        self.headset_model = data['headset_model']
        self.headset_sn = data['headset_sn']
    
    
    @classmethod
    def get_all_headsets(cls):
        query = """
            SELECT
                *
            FROM headsets;
        """
        result =  connectToMySQL(cls.db_name).query_db(query)
        headsets = []
        if result:
            for headset in result:
                headsets.append(headset)
        return headsets
    
    
    @classmethod
    def get_headset_by_id(cls, data):
        query = """
            SELECT
                *
            FROM headsets
            WHERE headset_id = %(headset_id)s;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return None
    
    
    @classmethod
    def update_headset(cls, data):
        query = """
            UPDATE headsets
            SET
                adapter_model = %(adapter_model)s,
                adapter_sn = %(adapter_sn)s,
                headset_model = %(headset_model)s,
                headset_sn = %(headset_sn)s
            WHERE headset_id = %(headset_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod    
    def delete_headset(cls, data):
        query = """
            DELETE FROM headsets
            WHERE headset_id = %(headset_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_headset(data):
        is_valid = True
        if len(data['adapter_model']) < 1:
            is_valid = False
            flash("Adapter model is required.", "headset_edit")
        if len(data['adapter_sn']) < 1:
            is_valid = False
            flash("Adapter serial number is required.", "headset_edit")
        if len(data['headset_model']) < 1:
            is_valid = False
            flash("Headset model is required.", "headset_edit")
        if len(data['headset_sn']) < 1:
            is_valid = False
            flash("Headset serial number is required.", "headset_edit")
        return is_valid
    