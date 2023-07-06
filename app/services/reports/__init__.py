from docxtpl import DocxTemplate
from datetime import datetime

def generate_doc():
    doc=DocxTemplate('price_template.docx')
    context={'data_de_hoje':datetime.now()}
    doc.render(context)
    doc.save('generated.docx')