import pyodbc
import datetime as dt
from mealslip.config import settings

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={settings.SQL_SERVER};DATABASE={settings.SQL_DB};"
        f"UID={settings.SQL_USER};PWD={settings.SQL_PASSWORD};"
        "TrustServerCertificate=yes;Connection Timeout=5;"
    )
    return pyodbc.connect(conn_str, autocommit=True, timeout=5)