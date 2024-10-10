from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Monitor:
    db_name = DB_NAME

    def __init__(self, data):
        self.monitor_id = data['monitor_id']
        self.model = data['model']
        self.model_sn = data['model_sn']
        self.size = data['size']
    
    
    @classmethod
    def get_all_monitors(cls):
        query = """
            SELECT
                *
            FROM monitors;
        """
        result =  connectToMySQL(cls.db_name).query_db(query)
        monitors = []
        if result:
            for monitor in result:
                monitors.append(monitor)
        return monitors
    
    
    @classmethod
    def get_monitor_by_serial_nr(cls, data):
        query = """
            SELECT
                *
            FROM monitors
            WHERE model_sn = %(model_sn)s;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return None
    
    
    @classmethod
    def update_monitor(cls, data):
        query = """
            UPDATE monitors
            SET
                model = %(model)s,
                model_sn = %(model_sn)s
        """
        if data['size'] != "" and data['size'] != None and data['size'] != "None":
            query += ", size = %(size)s"
        query += """
            WHERE monitor_id = %(monitor_id)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
        
    
    @classmethod
    def get_monitor_by_id(cls, data):
        query = """
            SELECT
                *
            FROM monitors
            WHERE monitor_id = %(monitor_id)s;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return None
    
    
    @classmethod
    def delete_monitor(cls, data):
        query = """
            DELETE FROM monitors
            WHERE monitor_id = %(monitor_id)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_monitor(data):
        is_valid = True
        if data['model'] == "" or data['model'] == None:
            is_valid = False
            flash("Model is required","monitor_edit")
        if data['model_sn'] == "" or data['model_sn'] == None:
            is_valid = False
            flash("Model SN is required","monitor_edit")
        if data['size'] == "" or data['size'] == None:
            is_valid = False
        return is_valid
    