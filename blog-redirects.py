import os
from pathlib import Path
import xml.etree.ElementTree as ET
import lxml.etree as LXML
import csv


scriptPath = Path(os.path.dirname(__file__))
os.chdir(scriptPath)

parser = LXML.XMLParser(strip_cdata=False)
xmlFile = LXML.parse(scriptPath / 'tru-dsmartuvc.WordPress.2023-07-10_published.xml', parser)
ns = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/'
}
root = xmlFile.getroot()

csvFilename = 'UVC360-redirects.csv'
redirectHeader = [
    'Legacy URL Pattern', 
    'Redirect To',
    'Match Type',
    'HTTP Status',
    'Site ID',
    'Legacy URL Match Type'
]

with open(scriptPath / csvFilename, 'w', encoding='UTF8', newline='') as f:

    writer = csv.writer(f)

    writer.writerow(redirectHeader)

    for idx, item in enumerate(root.findall('channel/item')):

        postName = item.find('wp:post_name', namespaces=ns)
        oldUrl = '/' + postName.text
        newUrl = '/blog' + oldUrl

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

