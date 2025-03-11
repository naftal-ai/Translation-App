import sqlite3

def create_database():
    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect("translation_app.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        word_id INTEGER PRIMARY KEY, 
        en_word TEXT NOT NULL, 
        part_of_speech TEXT NOT NULL, 
        translation TEXT NOT NULL, 
        audio_path TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inflections (
        inflection_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        inflection TEXT NOT NULL,
        FOREIGN KEY (word_id) REFERENCES words (word_id) ON DELETE CASCADE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS examples (
        example_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        example TEXT NOT NULL,
        FOREIGN KEY (word_id) REFERENCES words (word_id) ON DELETE CASCADE
    );
    """)

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

# Create the database
create_database()
