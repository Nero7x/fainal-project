import io
from PyPDF2 import PdfReader 
import spacy
import nltk as nltk
from server import ElemenrsFinder as EF
from server import ReletionshipFinder as RF


def dataInitialization(file,file_extension,diagram_type):
    print(diagram_type)
    texts = ""
    if file_extension == ".txt":
        text = file.read().decode('utf-8') 
        texts = nltk.sent_tokenize(text)

    elif file_extension ==".pdf":
        reader = PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        texts = nltk.sent_tokenize(text)
    nlp = spacy.load('en_core_web_sm')

    results = {}

    for text in texts:
        doc = nlp(text)
        actor = EF.ElementsFinder.findActor(doc)
        usecase = EF.ElementsFinder.findUsecase(doc,actor)
        ucr = RF.RelationshipFinder.findUsecaseRelationship(doc, actor)
        clas = EF.ElementsFinder.findClass(doc)
        attr = EF.ElementsFinder.findAttributes(doc)
        method = EF.ElementsFinder.findMethod(doc,actor)
        #cr = RF.RelationshipFinder.findClassRleationship(doc)

        results[text] = {
        'actors': actor,
        'usecases': usecase,
        'usecase relationship': ucr,
        'class': clas,
        'attributes': attr,
        'method' : method,
        }

    for i,result in enumerate(results):
        print(f"{i}- {result}: {results[result]}")



