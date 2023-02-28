from typing import Callable
from spacy.tokens.token import Token
from spacy.language import Language


def add_tokens(nlp: Language, stream):
    to_token: Callable[[Token], dict] = lambda t: {
        "id": t.i,
        "text": t.text,
        "start": t.idx,
        "end": t.idx + len(t.text) + 1,  # end index is exclusive.
    }

    for example in stream:
        doc = nlp(example["text"])
        tokens = [to_token(t) for t in doc]
        yield {"tokens": tokens, **example}
