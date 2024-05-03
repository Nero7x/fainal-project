import spacy
from spacy.matcher import Matcher

# تحميل نموذج spaCy
nlp = spacy.load('en_core_web_sm')


# الجمل للتحليل
texts = ["The user logs in to the system using their username and password.",
         "The admin updates the user's profile.",
         "The system sends a notification to the user.",
         "The user can change their password at any time.",
         "The system automatically logs out after a period of inactivity for 15 minutes.",
         "The admin can add or delete users from the system.",
         "The system stores all user data securely.",
         "The user can recover their password using their email address.",
         "The system verifies the user's email address before creating an account.",
         "The admin can view usage statistics for all users.",
         "The user can upload and download files.",
         "The system encrypts all sensitive data.",
         "The admin can reset a user's password.",
         "The user can update their profile picture.",
         "The system maintains a log of all user activity.",
         "The user can search for other users.",
         "The system provides two-factor authentication for added security.",
         "The admin can suspend or reactivate user accounts.",
         "The user can send messages to other users.",
         "The system sends a confirmation email after successful registration."]

# قاموس لتخزين النتائج
results = {}
for text in texts :
    doc = nlp(text)
    for token in doc.ents:
        print(f"{token.text} : {token.label_}")

# طباعة النتائج
