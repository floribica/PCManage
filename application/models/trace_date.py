from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Trace:
    db_name = DB_NAME

    def __init__(self, data):
        self.trace_date_id = data["trace_date_id"]
        self.authorization_date = data["authorization_date"]
        self.request_date = data["request_date"]
        self.approved_date = data["approved_date"]
        self.ready_date = data["ready_date"]
        self.submitted_date = data["submitted_date"]
        self.returned_date = data["returned_date"]
        self.cancel_date = data["cancel_date"]
        
    
    @classmethod
    def approve_request(cls, data):
        query = """
        UPDATE trace_date
        SET
            approved_date = %(approved_date)s
        WHERE trace_date_id = %(trace_date_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def cancel_request(cls, data):
        query = """
        UPDATE trace_date
        SET
            cancel_date = %(cancel_date)s
        WHERE trace_date_id = %(trace_date_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def ready_request(cls, data):
        query = """
        UPDATE trace_date
        SET
            ready_date = %(ready_date)s
        WHERE trace_date_id = %(trace_date_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def submitted_request(cls, data):
        query = """
        UPDATE trace_date
        SET
            submitted_date = %(submitted_date)s
        WHERE trace_date_id = %(trace_date_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def returned_request(cls, data):
        query = """
        UPDATE trace_date
        SET
            returned_date = %(returned_date)s
        WHERE trace_date_id = %(trace_date_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def add_request(cls, data):
        query = """
            INSERT INTO trace_date
                (request_date)
            VALUES
                (%(request_date)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def get_last_trace_date_id(cls):
        query = """
            SELECT
                trace_date_id
            FROM trace_date
            ORDER BY trace_date_id DESC
            LIMIT 1;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            return results[0]
        return None
    