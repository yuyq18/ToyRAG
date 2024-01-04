import pandas as pd

def format_text(text: str) -> str:
    return text.strip('\n').strip().replace('\n', '')

def format_docs(docs: pd.DataFrame) -> str:
    docs_text = []
    for i in range(len(docs)):
        text = ''
        for c in ["Title", "Body"]:
            text += c + ': ' + docs.loc[i, c] + ' '
        docs_text.append(text)
    return '\n'.join(docs_text)