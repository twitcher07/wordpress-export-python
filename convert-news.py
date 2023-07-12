import os
from pathlib import Path
import xml.etree.ElementTree as ET
import lxml.etree as LXML


scriptPath = os.path.realpath(os.path.dirname(__file__))
os.chdir(scriptPath)

parser = LXML.XMLParser(strip_cdata=False)
xmlFile = LXML.parse(os.path.join(scriptPath, 'tru-dsmartuvc.WordPress.2023-07-10_published.xml'), parser)
root = xmlFile.getroot()

for idx, item in enumerate(root.findall('channel/item')):

    categories = item.findall("category[@domain='category']")
    tags = item.findall("category[@domain='post_tag']")

    print('-----------------------------------')
    print(idx, ':', item.find('title').text)

    if categories:
        newCategoriesEl = LXML.SubElement(item, 'Categories')

        for cat in categories:
            newCategory = LXML.SubElement(newCategoriesEl, 'Category')
            newCategory.text = cat.text
        
        print(LXML.tostring(newCategoriesEl, encoding="unicode", pretty_print=True))

    if tags:
        newTagsEl = LXML.SubElement(item, 'Tags')

        for tag in tags:
            newTag = LXML.SubElement(newTagsEl, 'Tag')
            newTag.text = tag.text
        
        print(LXML.tostring(newTagsEl, encoding="unicode", pretty_print=True))

    print('-----------------------------------')

xmlFile.write(os.path.join(scriptPath, 'UVC360_published.xml'), pretty_print=True, encoding='UTF-8', xml_declaration=True)
