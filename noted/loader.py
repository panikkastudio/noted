import jsonlines


class JSONL:
    @staticmethod
    def load(path: str):
        return jsonlines.open(path).iter(type=dict, skip_invalid=True)
