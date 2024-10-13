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
    def add_computer(cls, data):
        # Base query with mandatory fields
        query = """
            INSERT INTO computers
                (serial_nr, model{extra_columns})
            VALUES
                (%(serial_nr)s, %(model)s{extra_values});
        """
        
        # Optional fields
        optional_fields = ['cpu', 'ram', 'storage_type', 'storage_value']
        
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
        
        
    @staticmethod
    def validate_computer(data):
        is_valid = True
        if data['serial_nr'] == "" or data['serial_nr'] == None:
            is_valid = False
        if data['model'] == "" or data['model'] == None:
            is_valid = False
        return is_valid
    