import mysql.connector
with open("E:/Ai/world_match_challenges/A8/Podcasts/Amirkabir_E31.mp3", "rb") as audio:
    data = audio.read()

con = mysql.connector.connect(host="localhost", user="root", database="podcast", connection_timeout=30)  # Timeout set to 30 seconds
cursor = con.cursor()
query = """INSERT INTO audio_files(id, name, img_address, audio_data)VALUES(%s, %s, %s, %s)"""
cursor.execute(query, (1, "امیرکبیر", "podcast_characters/AmirKabir_naghashbashi.jpg", data))
con.commit()
cursor.close()