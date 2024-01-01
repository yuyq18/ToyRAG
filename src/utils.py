import pandas as pd

def format_text(text: str) -> str:
    return text.strip('\n').strip().replace('\n', '')

def format_docs(docs: pd.DataFrame) -> str:
    docs_text = []
    for i in range(len(docs)):
        # text = ''
        # for c in docs.columns:
        #     text += c + ': ' + docs.loc[i, c] + ' '
        text = str(i) + '. ' + docs.loc[i, 'Description']
        docs_text.append(text)
    return '\n'.join(docs_text)