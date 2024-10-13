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
    
    
    @classmethod
    def get_all_pc_actions(cls):
        query = """
            SELECT
                *
            FROM pc_action;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        pc_actions = []
        if results:
            for pc_action in results:
                pc_actions.append(pc_action)
        return pc_actions
    
    
    @classmethod
    def procesverbal_data(cls, data):   
        query = """
            SELECT
                pc_action.*,
                hrs.*,
                computers.*,
                monitors.*,
                headsets.*,
                others.*,
                users.username
            FROM pc_action
            JOIN hrs ON pc_action.hr_id = hrs.hr_id
            JOIN computers ON pc_action.computer_sn = computers.serial_nr
            JOIN monitors ON pc_action.monitor_sn = monitors.monitor_sn
            JOIN headsets ON pc_action.headset_id = headsets.headset_id
            JOIN others ON pc_action.other_id = others.other_id
            JOIN users ON pc_action.user_id = users.user_id
            WHERE pc_action_id = %(pc_action_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return None
    