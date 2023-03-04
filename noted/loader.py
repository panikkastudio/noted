import jsonlines
from typing import Iterator


class JSONL:
    @staticmethod
    def load(path: str):
        return jsonlines.open(path).iter(type=dict, skip_invalid=True)


class Text:
    @staticmethod
    def load(path: str):
        with open(path, 'r') as f:
            for line in f:
                yield line

    @staticmethod
    def write(path: str, iter: Iterator[str]):
        with open(path, 'w') as f:
            for line in iter:
                f.write(f"{line}\n")