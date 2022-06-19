import spacy
from infrastruct.spacy_parser import *
from usecases.searcher import *


if __name__ == '__main__':
    parser = SpacyParser()
    searcher = Searcher(parser)
    searcher.search('Apple is looking at buying U.K. startup for $1 billion')
    print()
    searcher.search('Movies directed by Tom Hanks and acted by Robert de Niro betwen 1970 and 1980')
    print()
    searcher.search('Actors who have acted in the movies directed by Christopher Nolan')


    # searcher.search('Credit and mortgage account holders that submit their requests in January')

# import spacy
# from spacy import displacy
#
# text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
#
# nlp = spacy.load("en_core_web_sm")
# doc = nlp(text)
# displacy.serve(doc, style="ent")