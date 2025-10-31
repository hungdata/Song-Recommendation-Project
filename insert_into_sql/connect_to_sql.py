import pyodbc

server = "Your server"
database = "Your database"
username = "your username"
password = "your password"

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER='+server+';'
    'DATABASE='+database+';'
    'UID='+username+';'
    'PWD='+password
)

print("Kết nối thành công!")
cursor = conn.cursor()
