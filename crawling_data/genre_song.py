import pyodbc
import musicbrainzngs
import time

# ============================
# 1️⃣ Kết nối SQL Server
# ============================
server = "DESKTOP-5UJDEDV"
database = "spotify"
username = "sa"
password = "sa"

conn = pyodbc.connect(
    f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
cursor = conn.cursor()

# ============================
# 2️⃣ Thiết lập MusicBrainz
# ============================
musicbrainzngs.set_useragent("MusicGenreCollector", "1.0", "contact@example.com")

# ============================
# 3️⃣ Hàm lấy genre từ MusicBrainz
# ============================
def get_genre_from_musicbrainz(song_name, artist_name=None):
    try:
        # Tìm theo tên bài hát và nghệ sĩ (nếu có)
        if artist_name:
            result = musicbrainzngs.search_recordings(
                recording=song_name, artist=artist_name, limit=1
            )
        else:
            result = musicbrainzngs.search_recordings(recording=song_name, limit=1)

        if not result.get("recording-list"):
            # Nếu không tìm thấy, thử lại chỉ theo tên bài hát
            result = musicbrainzngs.search_recordings(recording=song_name, limit=1)
            if not result.get("recording-list"):
                return None

        record = result["recording-list"][0]
        artist_id = record["artist-credit"][0]["artist"]["id"]

        # Lấy thông tin nghệ sĩ bao gồm "tags" (chính là thể loại)
        artist_info = musicbrainzngs.get_artist_by_id(artist_id, includes=["tags"])
        tags = artist_info["artist"].get("tag-list", [])

        if tags:
            genres = [t["name"] for t in tags]
            return ", ".join(genres)
        return None

    except musicbrainzngs.NetworkError:
        print("🌐 Lỗi mạng, chờ 2 giây rồi thử lại...")
        time.sleep(2)
        return get_genre_from_musicbrainz(song_name, artist_name)
    except Exception as e:
        print(f"⚠️ Lỗi khi truy vấn {song_name}: {e}")
        return None

# ============================
# 4️⃣ Lấy danh sách bài hát từ DB
# ============================
cursor.execute("""
    SELECT TOP 20 Title, Artist
    FROM SpotifyTracks
    WHERE Genre IS NULL OR Genre = ''
""")

rows = cursor.fetchall()

# ============================
# 5️⃣ In kết quả ra màn hình
# ============================
for i, row in enumerate(rows, 1):
    title, artist = row
    print(f"\n🎵 [{i}] {title} - {artist}")
    genre = get_genre_from_musicbrainz(title, artist)
    if genre:
        print(f"   ➤ Genre: {genre}")
    else:
        print("   ❌ Không tìm thấy thể loại.")
    time.sleep(1.5)  # tránh giới hạn API (MusicBrainz ~1 request/giây)

print("\n✅ Hoàn thành tra cứu genre.")



