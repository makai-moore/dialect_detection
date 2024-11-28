import copy
from collections import Counter
import pandas as pd
import nltk

# put every document into a dictionary by id
doc_dict = {}
id_dict = {}

country_set = set()
sources_df = pd.read_excel("./text/sampleSources.xlsx", sheet_name="texts")
for text_id, (country_code, doc_type) in [(l[0], tuple(l[1].split())) for l in sources_df[["textID", "country|genre"]].values.tolist()]:
    with open(f"./text/w_{country_code.lower()}_{doc_type.lower()}.txt", 'r',
              encoding="utf-8") as file:
        # add each text id to id_dict
        if f"{country_code}_{doc_type}" not in id_dict:
            id_dict[f"{country_code}_{doc_type}"] = [text_id]
        else:
            id_dict[f"{country_code}_{doc_type}"].append(text_id)
        country_set.add(country_code)
        IS_DOC = False
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith(f"##{text_id}"):
                IS_DOC = True
            elif line.strip().startswith("##"):
                IS_DOC = False
            if IS_DOC:
                if text_id not in doc_dict:
                    doc_dict[text_id] = [w.lower() for w in nltk.word_tokenize(line)]
                else:
                    doc_dict[text_id] += [w.lower() for w in nltk.word_tokenize(line)]

# Replace only words that appear exactly once in the entire corpus with the <UNK> token
vocab = Counter({})
vocab['<UNK>'] = 0
for doc in doc_dict.values():
    for word in doc:
        if word in vocab:
            vocab[word] += 1
        else:
            vocab[word] = 1
for doc in doc_dict.values():
    for i, word in enumerate(doc):
        if vocab[word] == 1:
            doc[i] = '<UNK>'
            vocab['<UNK>'] += 1

# make sets for every country and record every word used by each country
vocab_sets = {country_code:set() for country_code in country_set}
for country_code in country_set:
    for text_id in id_dict[f"{country_code}_B"] + id_dict[f"{country_code}_G"]:
        for word in doc_dict[text_id]:
            vocab_sets[country_code].add(word)

# make new vocabulary sets, removing words that appear in less than 
# 25% and 50% of the countries datasets respectively
vocab_25 = vocab.copy()
vocab_50 = vocab.copy()
for word in vocab:
    COUNTRY_COUNT = 0
    for country_code in country_set:
        if word in vocab_sets[country_code]:
            COUNTRY_COUNT+=1
    if COUNTRY_COUNT / len(country_set) < 0.25:
        del vocab_25[word]
    if COUNTRY_COUNT / len(country_set) < 0.5:
        del vocab_50[word]

# Replace any words that appear in less than 25% of the countries’ datasets with the <UNK> token
doc_dict_25 = copy.deepcopy(doc_dict)
for text_id, doc in doc_dict_25.items():
    for i, word in enumerate(doc):
        if word not in vocab_25:
            print(text_id, word)
            doc_dict_25[text_id][i] = '<UNK>'
            vocab_25['<UNK>'] += 1

# Replace any words that appear in less than 50% of the countries’ datasets with the <UNK> token
doc_dict_50 = copy.deepcopy(doc_dict)
for text_id, doc in doc_dict_50.items():
    for i, word in enumerate(doc):
        if word not in vocab_50:
            print(text_id, word)
            doc_dict_50[text_id][i] = '<UNK>'
            vocab_50['<UNK>'] += 1
