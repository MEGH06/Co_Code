import spacy

nlp=spacy.load("en_core_web_sm")

def clean_text(text_list):
    for i in range(len(text_list)):
        text = text_list[i]
        doc=nlp(text)
        filtered_tokens=[]
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
            filtered_tokens.append(token.lemma_)
            text = " ".join(filtered_tokens)
        text_list[i] = text
    return text_list

# print(clean_text(["Hello, world!", "This is a test.", "The code is running.", "The cat ate the dog"]))
