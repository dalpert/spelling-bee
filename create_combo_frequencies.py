from bs4 import BeautifulSoup
import itertools
import pickle
from urllib.request import urlopen
import timeit

PICKLE_PATH = "data/pickles"


def generate_links() -> list[str]:
    # 2096 is hardcoded up to the latest day of Spelling Bee
    return [f"https://www.sbsolver.com/s/{i}" for i in range(1, 2096)]


def get_soup(link: str) -> BeautifulSoup:
    """Function to return the soup for a given link so we don't have to repeatedly call it in other
    functions and hit any rate limits.
    """
    with urlopen(link) as url:
        page = url.read()
    return BeautifulSoup(page, "html.parser")


def get_words(soup: BeautifulSoup) -> list[str]:
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


def get_center_letter(soup: BeautifulSoup) -> str:
    return soup.find_all(class_="bee-center")[1].text


def create_key(letters: set):
    return "".join(sorted(letters))


def get_letter_set(word: str) -> set:
    return set(c for c in word)


def update_combo_frequency(
    combo_frequency: dict, unique_letters: set, center_letter: str
) -> str:

    for i in range(1, 8):
        combos = list(itertools.combinations(unique_letters, i))
        for combo in filter(lambda x: center_letter in x, combos):
            key = create_key(combo)
            combo_frequency[key] = combo_frequency.get(key, 0) + 1


def add_words_to_word_dict(word_dict, word_lst):
    for word in word_lst:
        key = create_key(get_letter_set(word))
        if key in word_dict:
            word_dict[key].append(word)
        else:
            word_dict[key] = [word]


def pickle_data(var_name: str) -> None:
    file_path = f"{PICKLE_PATH}/{var_name.__name__}.pkl"
    with open(file_path, "wb") as file:
        pickle.dump(var_name, file)


def main():
    links = generate_links()
    word_dict = {}
    combo_frequency_dict = {}
    for link in links[:10]:
        soup = get_soup(link)
        center_letter = get_center_letter(soup)
        word_lst = get_words(soup)
        unique_letters = get_unique_letters(word_lst)
        update_combo_frequency(combo_frequency_dict, unique_letters, center_letter)
        add_words_to_word_dict(word_dict, word_lst)

    pickle_data(combo_frequency_dict)
    pickle_data(word_dict)


if __name__ == "__main__":
    elapsed_time = timeit.timeit(main, number=1)
    print(elapsed_time)
