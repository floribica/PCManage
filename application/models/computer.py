from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Computer:
    db_name = DB_NAME

    def __init__(self, data):
        self.serial_nr = data['serial_nr']
        self.model = data['model']
        self.cpu = data['cpu']
        self.ram = data['ram']
        self.storage_type = data['storage_type']
        self.storage_value = data['storage_value']


    @classmethod
    def get_all_computers(cls):
        query = """
            SELECT
                *
            FROM computers;
        """
        result =  connectToMySQL(cls.db_name).query_db(query)
        computers = []
        if result:
            for computer in result:
                computers.append(computer)
        return computers
    
    
    @classmethod
    def get_computer_by_serial_nr(cls, data):
        query = """
            SELECT
                *
            FROM computers
            WHERE serial_nr = %(serial_nr)s;
        """
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return (result[0])
        return None
    
    
    @classmethod
    def update_computer(cls, data):
        query = """
            UPDATE computers
            SET
                model = %(model)s
        """
        if data['cpu'] != "" and data['cpu'] != None and data['cpu'] != "None":
            query += ", cpu = %(cpu)s"
        if data['ram'] != "" and data['ram'] != None and data['ram'] != "None":
            query += ", ram = %(ram)s"
        if data['storage_type'] != "" and data['storage_type'] != None and data['storage_type'] != "None":
            query += ", storage_type = %(storage_type)s"
        if data['storage_value'] != "" and data['storage_value'] != None and data['storage_value'] != "None":
            query += ", storage_value = %(storage_value)s"
        query += " WHERE serial_nr = %(serial_nr)s;"
        
        connectToMySQL(cls.db_name).query_db(query, data)
        

    @classmethod
    def delete_computer(cls, data):
        query = """
            DELETE FROM computers
            WHERE serial_nr = %(serial_nr)s;
        """
        connectToMySQL(cls.db_name).query_db(query, data)
    