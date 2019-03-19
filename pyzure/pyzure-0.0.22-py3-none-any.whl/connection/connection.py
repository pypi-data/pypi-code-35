from pyzure.connection.azure_credentials import credential
import pyodbc


def connect(instance):
    credentials = credential(instance)
    cnxn = pyodbc.connect(**credentials)
    return cnxn
