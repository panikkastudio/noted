import spacy
import asyncio
import uvicorn
import logging

from logging import Logger
from noted.database import Database
from noted.loader import JSONL
from noted.server import create_server
from noted.recipe import BaseRecipe, RecipeManager
from noted.utils import set_hashes

## Temporary
from sense2vec import Sense2Vec


## Temporary (Going to make these command line argument)
task_name = "ner_occupations"
seeds = ["neighbour", "friend", "wife", "husband", "uncle"]
vector_path = "/Users/osman/Code/AmazonReview/reives_vectors/s2v_reddit_2019_lg"
case_sensitive = False
threshold = 0.85
n_similar = 100


logger = Logger("Sense2Vec Recipe")
logger.setLevel(logging.DEBUG)


class DummyRecipe(BaseRecipe):
    def __init__(self, database: Database) -> None:
        super().__init__(database)
        self._sequence = self.get_sequence()

    def get_next_task(self):
        return next(self._sequence)

    def get_config(self):
        return {"view_type": "text"}

    def get_sequence(self):
        dataset = "/Users/osman/Code/AmazonReview/reives_data/reviews_01_text.jsonl"
        data_sequence = JSONL.load(dataset)

        while True:
            entry = next(data_sequence)
            task = {"text": entry.get("text")}
            yield set_hashes(task)


class NERRecipe(BaseRecipe):
    def __init__(self, database: Database) -> None:
        super().__init__(database)
        self._sequence = self.get_sequence()

    def get_next_task(self):
        return next(self._sequence)

    def get_config(self):
        return {"view_type": "ner"}

    def get_sequence(self):
        dataset = "/Users/osman/Code/AmazonReview/reives_data/reviews_01_text.jsonl"
        data_sequence = JSONL.load(dataset)
        nlp = spacy.load("en_core_web_lg")

        while True:
            entry = next(data_sequence)
            text = entry.get("text")
            doc = nlp(text)

            to_span = lambda t: {
                "label": t.label_,
                "start": t.start_char,
                "end": t.end_char,
            }

            spans = [to_span(t) for t in doc.ents]
            task = {"text": text, "spans": spans}
            yield set_hashes(task)


class NERManualRecipe(BaseRecipe):
    def __init__(self, database: Database) -> None:
        super().__init__(database)
        self._sequence = self.get_sequence()

    def get_next_task(self):
        return next(self._sequence)

    def get_config(self):
        return {
            "view_type": "ner_manual",
            "labels": ["ROCCUP", "RTIME", "RREL"],
        }

    def get_sequence(self):
        dataset = "/Users/osman/Code/AmazonReview/reives_data/reviews_01_text.jsonl"
        data_sequence = JSONL.load(dataset)
        nlp = spacy.load("en_core_web_lg")

        while True:
            entry = next(data_sequence)
            text = entry.get("text")
            doc = nlp(text)

            to_span = lambda t: {
                "label": t.label_,
                "start": t.start_char,
                "token_start": t.start,
                "end": t.end_char,
                "token_end": t.end,
            }

            spans = [to_span(t) for t in doc.ents]
            task = {"text": text, "spans": spans}
            yield set_hashes(task)


class TextClassificationRecipe(BaseRecipe):
    def __init__(self, database: Database) -> None:
        super().__init__(database)
        self._sequence = self.get_sequence()
        self._database = database

    def get_next_task(self):
        return next(self._sequence)

    def get_config(self):
        return {
            "view_type": "classification",
            "choice_style": "single",
        }

    def get_sequence(self):
        dataset = "/Users/osman/Code/AmazonReview/reives_data/reviews_01_text.jsonl"
        data_sequence = JSONL.load(dataset)

        self._database.add_dataset("test-dataset")

        examples = self._database.get_examples("test-dataset")
        print("examples", examples)

        datasets = self._database.get_datasets()
        print("datasets", datasets)

        while True:
            entry = next(data_sequence)
            text = entry.get("text")
            yield set_hashes({"text": text, "label": "OCCUPATION"})


class Senve2VecRecipe(BaseRecipe):
    def __init__(self, database: Database) -> None:
        super().__init__(database)
        logger.debug("initialing the recipe")

        self._sequence = self.get_sequence()
        self._database = database

        self._init_tasks()
        logger.debug("initialized the recipe")

    def _init_tasks(self) -> None:
        """Initialize sense2vec etc."""
        self._seen = set()
        self._accept_keys = []
        self._seed_tasks = []

        logger.info("Initializing sense2vec")
        self._s2v = Sense2Vec().from_disk(vector_path)
        logger.info("Initialized sense2vec vectors")

        for seed in seeds:
            key = self._s2v.get_best_sense(seed)
            if key is None:
                logger.warn(f"Cannot find seed term '{seed}' in vectors.")
                continue

            self._accept_keys.append(key)
            best_word, best_sense = self._s2v.split_key(key)
            self._seen.add(best_word if case_sensitive else best_word.lower())

            task = {
                "text": key,
                "word": best_word,
                "sense": best_sense,
                "answer": "accept",
                "meta": {"score": 1.0, "sense": best_sense},
            }

            task = set_hashes(task)
            self._seed_tasks.append(task)

        if len(self._accept_keys) == 0:
            logger.error("No seeds available")
            return

    def get_sequence(self):
        """Return the sequence of tasks"""
        global threshold
        global most_similar
        global case_sensitive
        global n_similar

        while True:
            logger.info(
                f"looking for {n_similar} phrases most similar to "
                f"{len(self._accept_keys)} accepted keys"
            )

            n_skipped = 0
            n_duplicate = 0
            most_similar = self._s2v.most_similar(self._accept_keys, n=n_similar)

            for key, score in most_similar:
                if score > threshold:
                    word, sense = self._s2v.split_key(key)
                    is_duplicate = (case_sensitive and word in self._seen) or (
                        not case_sensitive and word.lower() in self._seen
                    )
                    if is_duplicate:
                        n_duplicate += 1
                        continue

                    self._seen.add(word if case_sensitive else word.lower())
                    # Make sure the score is a regular float, otherwise server
                    # may fail when trying to serialize it to/from JSON
                    meta = {"score": float(score), "sense": sense}
                    yield {"text": key, "word": word, "sense": sense, "meta": meta}

                else:
                    n_skipped += 1

            if n_skipped:
                logger.info(f"skipped {n_skipped} phrases below threshold {threshold}")

            if n_skipped == len(most_similar) - n_duplicate:
                # No most similar phrases were found that are above the
                # threshold, so lower the threshold if it's not already 0 or
                # return empty list so Prodigy shows "no tasks available"
                new_threshold = threshold - 0.1
                if new_threshold <= 0.0:
                    logger.info(f"no suggestions for threshold {threshold:.2}")
                    return None  # Signal recipe end.

                _msg = f"lowering threshold from {threshold:.2} to {new_threshold:.2}"
                logger.info(_msg)
                threshold = new_threshold

    def get_next_task(self):
        return next(self._sequence)

    def get_config(self):
        return {
            "view_type": "html",
            "html_template": "<span style='font-size: {{theme.largeText}}px'>{{ word }}</span>",
        }


if __name__ == "__main__":
    ## Preparation
    database = Database()

    ## Initialization
    recipe = NERManualRecipe(database=database)
    manager = RecipeManager(recipe)

    ## Run the server
    app = create_server(manager)
    config = uvicorn.Config(app, port=8000)
    server = uvicorn.Server(config)
    server.run()
