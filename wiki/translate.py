from transformers import pipeline
import pandas as pd
from tqdm import tqdm

model_checkpoint = "Helsinki-NLP/opus-mt-en-fr"
translator = pipeline("translation", model=model_checkpoint)
# print(translator("How are you?")[0]["translation_text"])

tqdm.pandas()


def translate(text):
    try:
        return translator(text)[0]["translation_text"]
    except:
        return "None"


def translate_dataset(path, save_path, N=10000):
    df = pd.read_csv(path, sep="\t").head(N)
    df['statement'] = df["statement"].progress_apply(translate)
    df = df[df['statement'] != "None"]
    df.to_csv(save_path, sep="\t")


folder = '/home/yonatan/Desktop/wikipedia'

if False:
    translate_dataset(folder + '/fake.tsv',
                      folder + '/translated_fake.tsv')

else:
    translate_dataset(folder + '/lqn_statements_cn_citations_sample.tsv',
                      folder + '/translated_lqn_statements_cn_citations_sample.tsv')

    translate_dataset(folder + '/fa_statements_no_citations_sample.tsv',
                      folder + '/translated_fa_statements_no_citations_sample.tsv')