import os
from docx import Document
import re

way, keyword, allins = input(), input(), 0
try:
    document = Document(way)
    for paragraph in document.paragraphs:
        allins += len(re.findall(keyword, paragraph.text, re.I))
except:
    pass
print(keyword + ": " + str(allins))