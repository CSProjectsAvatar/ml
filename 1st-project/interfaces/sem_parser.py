
from abc import ABC, abstractmethod
from typing import List


class SemParser(ABC):
    '''Semantic Parser Interface'''
    @abstractmethod
    def get_tags(self, query:str) -> List[str]:
        '''Returns the list with the tags corresponding to the parser analysis of the query(VERB, ADV, NOUN,...)'''
        pass
