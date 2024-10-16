from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class Upload:
    db_name = DB_NAME

    def __init__(self, data):
        self.upload_id = data["upload_id"]
        self.file = data["file"]
        self.pc_action_id = data["pc_action_id"]
        
        
    @classmethod
    def upload_procesverbal(cls, data):
        query = """
            INSERT INTO uploads
                (file, pc_action_id)
            VALUES
                (%(file)s, %(pc_action_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    