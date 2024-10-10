from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Hrs:
    db_name = DB_NAME

    def __init__(self, data):
        self.hr_id = data["hr_id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.statusi = data["statusi"]
        self.cancel_reason = data["cancel_reason"]
        self.request_id = data["request_id"]
        
    
    @classmethod
    def get_all_requests(cls):
        query = """
        SELECT
            hrs.*,
            trace_date.authorization_date
        FROM hrs
        JOIN trace_date
        ON hrs.trace_date_id = trace_date.trace_date_id
        WHERE statusi = 'request';
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        requests = []
        if results:
            for request in results:
                requests.append(request)
        return requests
    

    @classmethod
    def get_all_requests_trace(cls):
        query = """
        SELECT
            hrs.*,
            trace_date.authorization_date
        FROM hrs
        JOIN trace_date
        ON hrs.trace_date_id = trace_date.trace_date_id
        WHERE statusi != 'request';
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        requests = []
        if results:
            for request in results:
                requests.append(request)
        return requests
    
    
    @classmethod
    def get_trace_date_id(cls, data):
        query = """
        SELECT
            trace_date_id
        FROM hrs
        WHERE hr_id = %(hr_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return None
    
    
    @classmethod
    def approve_request(cls, data):
        query = """
        UPDATE hrs
        SET statusi = 'approved'
        WHERE hr_id = %(hr_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def ready_request(cls, data):
        query = """
        UPDATE hrs
        SET statusi = 'ready'
        WHERE hr_id = %(hr_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def submitted_request(cls, data):
        query = """
        UPDATE hrs
        SET statusi = 'submitted'
        WHERE hr_id = %(hr_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def returned_request(cls, data):
        query = """
        UPDATE hrs
        SET statusi = 'returned'
        WHERE hr_id = %(hr_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def cancel_request(cls, data):
        query = """
        UPDATE hrs
        SET 
            statusi = 'cancel',
            cancel_reason = %(reason)s
        WHERE hr_id = %(hr_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    