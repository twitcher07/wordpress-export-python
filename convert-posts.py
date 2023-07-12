import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import lxml.etree as LXML

exportFolder = 'exports'
if os.path.isdir(exportFolder) == False:
    os.mkdir(exportFolder)
scriptPath = Path(os.path.dirname(__file__))
os.chdir(scriptPath)

parser = LXML.XMLParser(strip_cdata=False)

while True:
    wordpressExportFile = input('Enter the file name or path to XML export from wordpress:\n')

    if wordpressExportFile.strip() != '' and os.path.isfile(wordpressExportFile):
        print('\n')
        wordpressExportFile = Path(wordpressExportFile)
        break
    elif wordpressExportFile.strip() != '' and os.path.isfile(wordpressExportFile) == False:
        print('[Error]: Can\'t find file at: ' + wordpressExportFile + '\n')
    else:
        print('[Error]: File name or path is required.\n')

exportXmlFileName = Path(exportFolder, wordpressExportFile.stem + '_transformed.xml')

if os.path.isfile(exportXmlFileName):
    print('[Error]: A file already exists by that name: ' + str(exportXmlFileName))
    print('Please, delete this file or rename it. And then try running this script again.')
    sys.exit()

xmlFile = LXML.parse(scriptPath / wordpressExportFile, parser)

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

xmlFile.write(scriptPath / exportXmlFileName, pretty_print=True, encoding='UTF-8', xml_declaration=True)
print('Converted XML file can be found at:', exportXmlFileName)
