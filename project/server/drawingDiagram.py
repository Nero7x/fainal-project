import os

def create_uml(variable):
    uml_text = f"""
    @startuml
    Alice -> Bob: Authentication Request
    Bob --> Alice: Authentication Response
    Alice -> Bob: Another authentication Request
    Alice <-- Bob: another authentication Response
    @enduml
    """
    with open('diagram.uml', 'w') as f:
        f.write(uml_text.format(variable=variable))

def generate_image():
    os.system("plantuml diagram.uml -o .")

# استخدم الدالة لإنشاء ملف uml
create_uml('متغير')
# استخدم الدالة لإنشاء الصورة
generate_image()


#def create_uml(uml_text):
    #with open('diagram.uml', 'w') as f:
        #f.write(uml_text)
