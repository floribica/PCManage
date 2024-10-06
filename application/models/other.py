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
    