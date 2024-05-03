from server import ElemenrsFinder as EF

class RelationshipFinder:

    def findUsecaseRelationship(doc):
        relationship = []
        actors = EF.ElementsFinder.findActor(doc)

        for token in doc:
            if token.pos_ == 'VERB':
                for child in token.children:
                    if child.pos_ == 'NOUN':
                        for actor in actors:
                            if child.text == actor:
                                relationship.append(f'Association({child.text} --- {token.text})')

        return relationship