from interfaces import sem_parser

class Searcher:
    def __init__(self, parser: sem_parser.SemParser) -> None:
        self.parser = parser

    def search(self, query: str):
        for tag in self.parser.get_tags(query):
            print(tag)


