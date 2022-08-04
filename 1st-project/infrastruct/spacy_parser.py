
from itertools import accumulate
from interfaces.sem_parser import *
from typing import List
import spacy
from spacy.symbols import nsubj, VERB

class SpacyParser(SemParser):
    def __init__(self) -> None:
        super().__init__()
        # self.nlp = en_core_web_sm.load()
        self.nlp = spacy.load("en_core_web_sm")
        # self.nlp = spacy.load("en")

    def get_tags(self, query: str) -> List[str]:
        doc = self.nlp(query)
        tagList = []
        for token in doc:
            tagList.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_alpha, token.is_stop])

        # Substitute taglist from ent.start to ent.end with the entity info
        words_less = 0
        for ent in doc.ents:
            tagList = tagList[:ent.start - words_less] + [[ent.text,'ENTITY', ent.label_]] + tagList[ent.end - words_less:]
            words_less += ent.end - ent.start - 1

        parent_list = __get_parent_tags(doc)
        print(parent_list)
        
        return tagList

    def __get_parent_tags(self, spacy_doc):
        parent = {}
        # Get the parent of each token
        for token in doc:
            for children in token.children:
                parent[children] = token.text