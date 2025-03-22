#!/usr/bin/env python3
import sqlite3
import requests
import os
from playsound3 import playsound

class Word:

    BASE_PATH = os.path.join(os.getcwd(), 'data')
    DB_FILE = 'translation_app.db'
    def __init__(self,
                 word_id: int,
                 en_word: str,
                 part_of_speech: str,
                 translation: str,
                 audio_path: (str | None) = None,
                 inflections: (list[str] | None) = None,
                 examples: (list[str] | None) = None
                 ) -> None:

        self.word_id: int = word_id
        self.en_word: str = en_word
        self.part_of_speech: str = part_of_speech
        self.translation: str = translation
        self.audio_path: (str | None) = audio_path
        self.inflections: list[str] = inflections if inflections else []
        self.examples: list[str] = examples if examples else []

    def play_word(self):
        try:
            """ Fetch the sound from the url """
            response = requests.get(self.audio_path, stream=True)
            response.raise_for_status()

            output_file = os.path.join(self.BASE_PATH,f'{self.word_id}.wav')
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            playsound(output_file)

            #remove the file after sounding it
            os.remove(output_file)





        except requests.exceptions.RequestException as e:
            print(f"Error fetching audio. \n{e}")


    def save_to_db(self, db_path=None):
        if db_path is None:
            db_path = Word.get_db_path()
        """Save the word object to the database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Insert into words table
            cursor.execute("""
            INSERT INTO words (word_id, en_word, part_of_speech, translation, audio_path)
            VALUES (?, ?, ?, ?, ?);
            """, (self.word_id, self.en_word, self.part_of_speech, self.translation, self.audio_path))

            # Insert inflections
            for inflection in self.inflections:
                cursor.execute("""
                INSERT INTO inflections (word_id, inflection)
                VALUES (?, ?);
                """, (self.word_id, inflection))

            # Insert examples
            for example in self.examples:
                cursor.execute("""
                INSERT INTO examples (word_id, example)
                VALUES (?, ?);
                """, (self.word_id, example))

            conn.commit()
            print(f"Word '{self.en_word}' saved successfully.")

        except sqlite3.IntegrityError as e:
            print(f"Error saving word '{self.en_word}': {e}")

        finally:
            conn.close()

    def delete_from_db(self, db_path=None):
        if db_path is None:
            db_path = Word.get_db_path()
        """
        Delete the word and its related entries (inflections and examples) from the database.
        """
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Delete the word from the `words` table
            cursor.execute("""
            DELETE FROM words WHERE word_id = ?;
            """, (self.word_id,))

            # delete inflections
            cursor.execute("""
            DELETE FROM inflections WHERE word_id = ?;
            """, (self.word_id,))

            # Delete Examples
            cursor.execute("""
            DELETE FROM examples where word_id = ?;
            """, (self.word_id,))

            conn.commit()
            print(f"Word '{self.en_word}' (ID: {self.word_id}) deleted successfully.")

        except sqlite3.Error as e:
            print(f"Error deleting word '{self.en_word}': {e}")

        finally:
            conn.close()

    @classmethod
    def get_from_db(cls, en_word, db_path=None) -> list[classmethod]:
        if db_path is None:
            db_path = cls.get_db_path()

        
        """Retrieve a word object from the database by English word."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Fetch word details
            cursor.execute("""
            SELECT * FROM words WHERE en_word = ?;
            """, (en_word,))

            word_rows: list[tuple] = cursor.fetchall()

            words = []

            if len(word_rows) == 0:
                print(f"No entries found for '{en_word}'.")
                return []

            for word_row in word_rows:
                word_id, en_word, part_of_speech, translation, audio_path = word_row

                # Fetch inflections
                cursor.execute("""
                SELECT inflection FROM inflections WHERE word_id = ?;
                """, (word_id,))
                inflections: list[str] = [row[0] for row in cursor.fetchall()]

                # Fetch examples
                cursor.execute("""
                SELECT example FROM examples WHERE word_id = ?;
                """, (word_id,))
                examples: list[str] = [row[0] for row in cursor.fetchall()]

                # Create and return Word object
                words.append(cls(word_id, en_word, part_of_speech, translation, audio_path, inflections, examples))

            return words

        finally:
            conn.close()
    
    @classmethod
    def get_db_path(cls):
        return os.path.join(cls.BASE_PATH, cls.DB_FILE) 
    
    def __str__(self):
        """String representation of the Word object."""
        return (f"Word ID: {self.word_id}\n"
                f"English Word: {self.en_word}\n"
                f"Part of Speech: {self.part_of_speech}\n"
                f"Translation: {self.translation}\n"
                f"Audio Path: {self.audio_path}\n"
                f"Inflections: {self.inflections}\n"
                f"Examples: {self.examples}")
