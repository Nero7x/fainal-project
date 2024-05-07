import unittest
import spacy
from server import ElemenrsFinder as EF
from server import ReletionshipFinder as RF


class TestFindActor(unittest.TestCase):
    def setUp(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = self.nlp("The user logs in to the system using their username and password.")

    def test_findActor(self):
        self.assertEqual(EF.ElementsFinder.findActor(self.doc), {"user"})

    def test_findUsecase(self):
        self.assertEqual(EF.ElementsFinder.findUsecase(self.doc ,EF.ElementsFinder.findActor(self.doc)), ["login"])

    def test_findUsecaseRelationship(self):
        self.assertEqual(RF.RelationshipFinder.findUsecaseRelationship(self.doc ,EF.ElementsFinder.findActor(self.doc)), ["user --> login"])

    def test_findClass(self):
        self.assertEqual(EF.ElementsFinder.findClass(self.doc), {"user"})

    def test_findAttributes(self):
        self.assertEqual(EF.ElementsFinder.findAttributes(self.doc), ["username", "password"])

    def test_findMethod(self):
        self.assertEqual(EF.ElementsFinder.findMethod(self.doc, EF.ElementsFinder.findActor(self.doc)), ["login"])

if __name__ == '__main__':
    unittest.main()
