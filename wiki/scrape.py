# https://medium.com/@Alexander_
# H/scraping-wikipedia-with-python-8000fc9c9e6c

import wikipedia
import re
import tqdm
import json
import nltk
from nltk import tokenize
import pandas as pd

nltk.download('punkt')

# page = wikipedia.page(title="Cosmébio")
# text = page.content.split(".")
# cn_samples.extend(re.findall(r"(?s)((?:[^\n][\n]?)+)\[réf. nécessaire\]", page.content))

max_nb_samples = 1000
wikipedia.set_lang('fr')
samples = []

pages = open("../fr_ebauches/société_ebauches.txt", "r").read().splitlines()
pages.extend(list(pd.read_csv("../fr_ebauches/french_ebauches.tsv", sep="\t")["title"].values))

for item in tqdm.tqdm(pages):
    try:
        item = " ".join(item.split())
        page = wikipedia.page(title=item)
        text = page.content.split(".")
        patterns = [
            r"\[réf. souhaitée\]",
            r"\[citation nécessaire\]",
            r"\[réf. à confirmer\]",
            r"\[réf. nécessaire\]",
            r"\[réf. nécessaire\]",
            r"\[source insuffisante\]",
        ]
        for pattern in patterns:
            # texts = re.findall(rf"[^.!?]*{pattern}", page.content)
            paragraphs = re.findall(rf"(?s)((?:[^\n][\n]?)+){pattern}", page.content)
            for paragraph in paragraphs:
                last_sentence = tokenize.sent_tokenize(paragraph)[-1]
                samples.append({"sentence": last_sentence,
                                "context": paragraph,
                                "page": item,
                                "reason": pattern})
                print(len(samples), "samples")
    except Exception as e:
        continue
    if len(samples) > max_nb_samples:
        break

with open("../french_ebauches_statements_citation_needed.json", "w") as file:
    json.dump(samples, file, ensure_ascii=False)
