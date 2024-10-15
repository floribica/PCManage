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
    def get_all_approved_request(cls):
        query = """
        SELECT
            hrs.*,
            trace_date.authorization_date
        FROM hrs
        JOIN trace_date
        ON hrs.trace_date_id = trace_date.trace_date_id
        WHERE statusi = 'approved';
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
    
    
    @classmethod
    def get_operator_info(cls, data):
        query = """
        SELECT
            fushata
        FROM hrs
        WHERE hr_id = %(hr_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return None
    
    
    @classmethod
    def get_cancel_reason(cls, data):
        query = """
        SELECT
            cancel_reason
        FROM hrs
        WHERE hr_id = %(hr_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]["cancel_reason"]
        return None
    
    
    @classmethod
    def add_request(cls, data):
        query = """
        INSERT INTO hrs
            (first_name, last_name, email, fushata, trace_date_id)
        VALUES
            (%(first_name)s, %(last_name)s, %(email)s, %(fushata)s, %(trace_date_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_add_request(data):
        is_valid = True
        if not data["first_name"]:
            flash("First name is required.", "add_request")
            is_valid = False
        if not data["last_name"]:
            flash("Last name is required.", "add_request")
            is_valid = False
        if not data["email"]:
            flash("Email is required.", "add_request")
            is_valid = False
        if not data["fushata"]:
            flash("Fushata is required.", "add_request")
            is_valid = False
        return is_valid
    