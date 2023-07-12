import os
from pathlib import Path
import xml.etree.ElementTree as ET
import lxml.etree as LXML
import csv

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
        break
    elif wordpressExportFile.strip() != '' and os.path.isfile(wordpressExportFile) == False:
        print('[Error]: Can\'t find file at: ' + wordpressExportFile + '\n')
    else:
        print('[Error]: File name or path is required.\n')

while True:
    exportCsvFileName = input('Enter a file name for the CSV file:\n')

    if exportCsvFileName.strip() != '': 
        exportCsvFileName = Path(exportFolder, exportCsvFileName + '.csv')

        if exportCsvFileName.is_file() == False:
            break
        elif exportCsvFileName.is_file():
            print('[Error]: A file already exists by that name.\n')
    else:
        print('[Error]: CSV file name is required.\n')

xmlFile = LXML.parse(scriptPath / wordpressExportFile, parser)
ns = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'wfw': 'http://wellformedweb.org/CommentAPI/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}
root = xmlFile.getroot()

redirectHeader = [
    'Legacy URL Pattern', 
    'Redirect To',
    'Match Type',
    'HTTP Status',
    'Site ID',
    'Legacy URL Match Type'
]

with open(scriptPath / exportCsvFileName, 'w', encoding='UTF8', newline='') as f:

    writer = csv.writer(f)

    writer.writerow(redirectHeader)

    for idx, item in enumerate(root.findall('channel/item')):

        postName = item.find('wp:post_name', namespaces=ns)
        oldUrl = '/' + postName.text
        newUrl = '/blog' + oldUrl ## new path that will prepend to the existing post_name

        print('-----------------------------------')
        print(idx, ':', item.find('title').text)
        print(postName.text, '->', '/blog/' + postName.text)
        writer.writerow([
            oldUrl,
            newUrl,
            'exactmatch',
            301,
            '',
            'pathonly'
        ])
        print('-----------------------------------')

    print('Redirect CSV file can be found at:', exportCsvFileName)

