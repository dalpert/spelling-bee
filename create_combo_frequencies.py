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
    for link in spelling_bee_links[:30]:
        soup = get_soup(link)
        center_letter = get_center_letter(soup)
        word_lst = get_words(soup)
        # update_combo_frequency(combo_frequency, unique_letters, center_letter)
    # file_path = f"{PICKLE_PATH}/combo_frequency.pkl"
    # with open(file_path, "wb") as file:
    #     pickle.dump(combo_frequency, file)


if __name__ == "__main__":
    elapsed_time = timeit.timeit(main, number=1)
    print(elapsed_time)
