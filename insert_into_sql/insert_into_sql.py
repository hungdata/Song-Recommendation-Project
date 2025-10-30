import pyodbc
server = ""
database = ""
username = ""
password = ""
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=' + server + ';'
    'DATABASE=' + database + ';'
    'UID=' + username + ';'
    'PWD=' + password
)
cursor = conn.cursor()
print("✅ Kết nối SQL thành công!")
# 2. Ghi vào SQL
cursor.execute("""
INSERT INTO SpotifyTracks 
(Artist, Title, Wks, T10, PK, Pkstreams, Total, ReleaseDate, Popularity)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (artist_name, title, wks, t10, pk, pkstreams, total, release_date, popularity))
conn.commit()
