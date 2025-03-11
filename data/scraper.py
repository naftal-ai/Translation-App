import requests
from bs4 import BeautifulSoup

from data.Word import Word


def fetch_data(word: str):
    base_url = "https://www.morfix.co.il"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(f"{base_url}/{word}", headers=headers)
        response.raise_for_status()

        return response

    except Exception as e:
        print("failed to scrape morfix", e)


def scraper(word: str) -> list[Word]:
    res = fetch_data(word)

    soup = BeautifulSoup(res.content, 'html.parser')

    # CSS selector to find elements start with 'word_' in their id
    en_words = soup.select("[id^='word_']")

    words: list[Word] = []

    for i, w in enumerate(en_words, start=1):
        # print(f"\n#{i}:")
        # get the word
        en_word = w.select_one("span.Translation_spTop_enTohe").text.strip()
        # print(f"en_word: {en_word}")

        # get the part of speech
        pos = w.select_one("span.Translation_sp2Top_enTohe").text.strip()
        # print(f"Part of Speech: {pos}")

        # get the inflections
        inflections: list[str] = w.select_one("div.Translation_div2center_enTohe").text.strip().split(',')
        inflections: list[str] = [i.strip() for i in inflections]
        # print(f"inflections: {inflections}")

        # get the translation
        translation = w.select_one('div.normal_translation_div').text.strip()
        # print(f"translation: {translation}")

        # get Examples of using
        examples = w.select("li > span.SampleSentences_text")
        examples = [e.text for e in examples]
        # print(f"examples: {examples}")

        # get the sound
        word_id = int(w["id"].split('_')[-1].strip())
        # print(f"Word ID = {word_id}")

        word = Word(
            word_id=word_id,
            en_word=en_word,
            part_of_speech=pos,
            translation=translation,
            audio_path=f"https://services.morfix.co.il/BritannicaAppSettings/Settings/GetSoundByMelingoID/{word_id}",
            inflections=inflections,
            examples=examples
        )

        words.append(word)

    return words

if __name__ == "__main__":
    word = input("enter word to translate: ")
    words: list[Word] = scraper(word)



