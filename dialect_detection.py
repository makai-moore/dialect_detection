import pandas as pd

vocab = {}
id_dict = {}

# put every document into a dictionary by id
doc_dict = {}
sources_df = pd.read_excel("./text/sampleSources.xlsx", sheet_name="texts")
for text_id, (country_code, doc_type) in \
    [(l[0], tuple(l[1].split())) for l in sources_df[["textID", "country|genre"]].values.tolist()]:
    with open(f"./text/w_{country_code.lower()}_{doc_type.lower()}.txt", 'r',
              encoding="utf-8") as file:
        # add each text id to id_dict
        if f"{country_code}_{doc_type}" not in id_dict:
            id_dict[f"{country_code}_{doc_type}"] = [text_id]
        else:
            id_dict[f"{country_code}_{doc_type}"].append(text_id)
        IS_DOC = False
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith(f"##{text_id}"):
                IS_DOC = True
            elif line.strip().startswith("##"):
                IS_DOC = False
            if IS_DOC:
                if text_id not in doc_dict:
                    doc_dict[text_id] = line
                else:
                    doc_dict[text_id] += line

for text_id in id_dict["AU_G"]:
    print(doc_dict[text_id])
