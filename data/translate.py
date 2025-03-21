#!/usr/bin/env python3
from data.scraper import scraper
from data.Word import Word

def get_translation(word) -> list[Word]:

    result: list[Word] = Word.get_from_db(word)

    if len(result) < 1:
        # Scrape the translation and add it to the database
        result: list[Word] = scraper(word)
        [w.save_to_db() for w in result]

    return result

if __name__ == "__main__":
    word = input("enter word to translate: ")
    words: list[Word] = get_translation(word)

    [print(w) for w in words]