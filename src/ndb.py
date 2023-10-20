from typing import List

import thirdai
from thirdai import neural_db as ndb


class ThirdAI:

    def __init__(self, api_key: str):
        thirdai.licensing.activate(api_key=api_key)
        self._db = ndb.NeuralDB()

    def insert(self, filenames: List[str]):
        sources = [ndb.PDF(fn) for fn in filenames]
        self._db.insert(
            sources=sources,
            train=True
        )

    def search(self, query: str, top_k: int):
        return self._db.search(query=query, top_k=top_k)


if __name__ == '__main__':
    filename = 'data/raw/2020-Scrum-Guide-US.pdf'
    thirdai = ThirdAI()
    thirdai.insert(filenames=[filename])

    results = thirdai.search(query='what are the main pillars of scrum', top_k=2)
    for result in results:
        print(result.text)
