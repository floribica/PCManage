from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Monitor:
    db_name = DB_NAME

    def __init__(self, data):
        self.monitor_sn = data['monitor_sn']
        self.model = data['model']
        self.size = data['size']
    
    
    @classmethod
    def add_monitor(cls, data):
        # Base query with mandatory fields
        query = """
            INSERT INTO monitors
                (model, monitor_sn{extra_columns})
            VALUES
                (%(model)s, %(monitor_sn)s{extra_values});
        """
        
        # Initialize optional column and value parts
        extra_columns = ""
        extra_values = ""
        
        # Check if 'size' is provided, if so, include it in the query
        if 'size' in data and data['size'] is not None:
            extra_columns = ", size"
            extra_values = ", %(size)s"
        
        # Format the query with optional 'size' if provided
        query = query.format(extra_columns=extra_columns, extra_values=extra_values)
        
        # Execute the query
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    
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
            WHERE monitor_sn = %(monitor_sn)s;
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
                monitor_sn = %(monitor_sn)s
        """
        if data['size'] != "" and data['size'] != None and data['size'] != "None":
            query += ", size = %(size)s"
        query += """
            WHERE monitor_sn = %(monitor_sn)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
        
    
    @classmethod
    def get_monitor_by_id(cls, data):
        query = """
            SELECT
                *
            FROM monitors
            WHERE monitor_sn = %(monitor_sn)s;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return None
    
    
    @classmethod
    def delete_monitor(cls, data):
        query = """
            DELETE FROM monitors
            WHERE monitor_sn = %(monitor_sn)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_monitor(data):
        is_valid = True
        if data['model'] == "" or data['model'] == None:
            is_valid = False
            flash("Model is required","monitor_edit")
        if data['monitor_sn'] == "" or data['monitor_sn'] == None or not data['monitor_sn']:
            is_valid = False
            flash("Model SN is required","monitor_edit")
        if data['size'] == "" or data['size'] == None:
            is_valid = False
        return is_valid
    