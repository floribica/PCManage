from flask import flash
from application.config.load_db import load_db
from application.config.mysqlconnection import connectToMySQL


DB_NAME = load_db()


class PC_Action:
    db_name = DB_NAME

    def __init__(self, data):
        self.pc_action_id = data["pc_action_id"]
        self.statusi = data["statusi"]
        self.fushata = data["fushata"]
        self.hr_id = data["hr_id"]
        self.computer_sn = data["computer_sn"]
        self.headset_id = data["headset_id"]
        self.monitor_sn = data["monitor_sn"]
        self.other_id = data["other_id"]
        self.user_id = data["user_id"]
        
    
    @classmethod
    def add_pc_action(cls, data):
        query = """
            INSERT INTO pc_action
                (fushata, hr_id, computer_sn, headset_id, monitor_sn, other_id)
            VALUES
                (%(fushata)s, %(hr_id)s, %(computer_sn)s, %(headset_id)s, %(monitor_sn)s, %(other_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    