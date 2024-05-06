from server import ElemenrsFinder as EF

class RelationshipFinder:

    def findUsecaseRelationship(doc, actors):
        relationship = []
        for token in doc:
            if token.pos_ == 'VERB':
                for child in token.children:
                    if child.pos_ == 'NOUN':
                        for actor in actors:
                            if child.text == actor:
                                relationship.append(f'{child.text} --> {token.text}')
        return relationship
    


    def findClassRleationship():
        
        return