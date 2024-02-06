from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib
import urllib.request
import itertools
import datetime
import pickle
from urllib.request import urlopen

PICKLE_PATH = "data/pickles"


def generate_links() -> list[str]:
    # 2096 is hardcoded up to the latest day of Spelling Bee
    return [f"https://www.sbsolver.com/s/{i}" for i in range(1, 2096)]


def get_words(link: str) -> list[str]:
    with urlopen(link) as url:
        page = url.read()
    soup = BeautifulSoup(page, "html.parser")
    answer_lst = soup.find_all(class_="bee-set")
    word_rows = answer_lst[0].find_all("tr")[1:]
    word_lst = []
    for word_row in word_rows:
        word = word_row.find_all("td")[0].text
        word_lst.append(word.upper())
    return word_lst


def get_unique_letters(word_lst: list[str]) -> set:
    unique_letters = set()
    for word in word_lst:
        unique_letters.update(set(word))
    return unique_letters


def get_center_letter(word_lst: list[str]) -> str:
    common_letters = set(word_lst[0])

    # Find the intersection of sets for each subsequent word
    for word in word_lst[1:]:
        common_letters.intersection_update(set(word))

    # Print or use the common letter(s)
    assert len(common_letters) == 1
    return list(common_letters)[0]


def update_combo_frequency(
    combo_frequency: dict, unique_letters: set, center_letter: str
) -> str:
    def create_key(letters: set):
        return "".join(sorted(letters))

    for i in range(1, 8):
        combos = list(itertools.combinations(unique_letters, i))
        for combo in filter(lambda x: center_letter in x, combos):
            key = create_key(combo)
            combo_frequency[key] = combo_frequency.get(key, 0) + 1


def main():
    spelling_bee_links = generate_links()
    combo_frequency = {}
    for link in spelling_bee_links[:20]:
        words = get_words(link)
        unique_letters = get_unique_letters(words)
        center_letter = get_center_letter(words)
        update_combo_frequency(combo_frequency, unique_letters, center_letter)
    file_path = f"{PICKLE_PATH}/combo_frequency.pkl"
    with open(file_path, "wb") as file:
        pickle.dump(combo_frequency, file)


if __name__ == "__main__":
    main()
