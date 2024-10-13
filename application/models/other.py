from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Other:
    db_name = DB_NAME

    def __init__(self, data):
        self.other_id = data['other_id']
        self.mouse = data['mouse']
        self.keyboard = data['keyboard']
        self.dp_vga = data['dp_vga']
        self.ac = data['ac']
        self.lan = data['lan']
        self.created_at = data['created_at']
    
    
    @classmethod
    def add_other(cls, data):
        query = """
            INSERT INTO others
                (created_at, model{extra_columns})
            VALUES
                (NOW(), %(model)s{extra_values});
        """
        
        # Optional fields
        optional_fields = ['mouse', 'keyboard', 'dp_vga', 'ac', 'lan']
        
        # Dynamic parts for optional columns and values
        extra_columns = ""
        extra_values = ""
        
        # Add optional fields if present in data
        for field in optional_fields:
            if field in data and data[field] is not None:
                extra_columns += f", {field}"
                extra_values += f", %({field})s"
        
        # Format query with additional columns/values if necessary
        query = query.format(extra_columns=extra_columns, extra_values=extra_values)
        
        # Execute the query
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def get_all_others(cls):
        query = """
            SELECT
                *
            FROM others;
        """
        result =  connectToMySQL(cls.db_name).query_db(query)
        others = []
        if result:
            for other in result:
                others.append(other)
        return others
    
    
    @classmethod
    def update_other(cls, data):
        query = """
            UPDATE others
            SET
        """
        if data['mouse'] != "" and data['mouse'] != None and data['mouse'] != "None":
            query += "mouse = %(mouse)s "
        if data['keyboard'] != "" and data['keyboard'] != None and data['keyboard'] != "None":
            query += ", keyboard = %(keyboard)s "
        if data['dp_vga'] != "" and data['dp_vga'] != None and data['dp_vga'] != "None":
            query += ", dp_vga = %(dp_vga)s "
        if data['ac'] != "" and data['ac'] != None and data['ac'] != "None":
            query += ", ac = %(ac)s "
        if data['lan'] != "" and data['lan'] != None and data['lan'] != "None":
            query += ", lan = %(lan)s "
        query += "WHERE other_id = %(other_id)s;"

        connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def get_other_by_id(cls, data):
        query = """
            SELECT
                *
            FROM others
            WHERE other_id = %(other_id)s;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None
    
    
    @classmethod
    def delete_monitor(cls, data):
        query = """
            DELETE FROM others
            WHERE other_id = %(other_id)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
        
    
    @classmethod
    def get_other_id(cls, data):
        query = """
            SELECT
                other_id
            FROM others
            ORDER BY other_id DESC
            LIMIT 1;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return None
    
    
    @staticmethod
    def validate_other(data):
        is_valid = True
        if not data['mouse'] and data['mouse'] == "" and data['mouse'] == "None":
            is_valid = False
            flash("Mouse is required", "other_edit")
        if not data['keyboard'] and data['keyboard'] == "" and data['keyboard'] == "None":
            is_valid = False
            flash("Keyboard is required", "other_edit")
        if not data['dp_vga'] and data['dp_vga'] == "" and data['dp_vga'] == "None":
            is_valid = False
            flash("DP/VGA is required", "other_edit")
        if not data['ac'] and data['ac'] == "" and data['ac'] == "None":
            is_valid = False
            flash("AC is required", "other_edit")
        if not data['lan'] and data['lan'] == "" and data['lan'] == "None":
            is_valid = False
            flash("LAN is required", "other_edit")
        return is_valid
    