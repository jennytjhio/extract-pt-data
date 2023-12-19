import requests
from bs4 import BeautifulSoup

link = "https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_negeri_di_Indonesia"

html = requests.get(link).text

soup = BeautifulSoup(html, "html.parser")

all_a_tags = soup.find_all("a")

all_universities = []
for a_tag in all_a_tags:
    # check if a_tag parent is a <li> tag and grandparent is a <ul> tag and it doesn't have a previous sibling of a
    if (
        a_tag.parent.name == "li"
        and a_tag.parent.parent.name == "ul"
        and a_tag.find_previous_sibling("a") is None
        and a_tag.find_next_sibling("a") is not None
    ):
        all_universities.append(a_tag)

with open("universitas_negeri.txt", "w") as file:
    for university in all_universities:
        file.write(university.text + "\n")
