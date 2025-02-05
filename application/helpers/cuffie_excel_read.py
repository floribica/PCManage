from flask import flash
import pandas as pd

from application.models.del_headset import Del_Headset

def upload_cuffie_excel(file):
    df = pd.read_excel(file)
    #get the columns of the excel file
    columns = df.columns
    #check if the columns are correct
    if columns[1] != "Nome" or columns[2] != "Cognome" or columns[3] != "Seriale cuffie":
        flash("Invalid file formatt","del_add")
        return
    #get the values of the excel file
    values = df.values
    for value in values:
        if value[6] == "RIKTHYER":
            statusi=1
        else:
            statusi=0
        data = {
            "headset_sn": value[3],
            "operator": value[1] + " " + value[2],
            "statusi": statusi,
            "user_id": 1
        }
        Del_Headset.upload_del_headset(data)
    flash("Data added successfully","del_add")