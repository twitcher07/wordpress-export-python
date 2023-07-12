import os
import time
import shutil
from pathlib import Path
import urllib.parse as urlparse
from urllib.request import url2pathname
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import lxml.etree as LXML
from requests import get

def download(url, file_name):
    # open in binary mode
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    with open(file_name, "wb") as file:
        # get request
        response = get(url, headers=headers)
        # write to file
        print('downloading: ' + url + ' to ' + file_name)
        file.write(response.content)

textFileName = 'UVC360-images.txt'
scriptPath = Path(os.path.dirname(__file__))
os.chdir(scriptPath)

ns = {
    'content': 'http://purl.org/rss/1.0/modules/content/'
}
parser = LXML.XMLParser(strip_cdata=False)
xmlFile = LXML.parse(scriptPath / 'tru-dsmartuvc.WordPress.2023-07-10_published.xml', parser)
root = xmlFile.getroot()
images = []
itemsWithImages = {}

for idx, item in enumerate(root.findall('channel/item'), 1):

    content = item.find('content:encoded', namespaces=ns)

    print('-----------------------------------')
    print(idx, ':', item.find('title').text)

    if content.text:
        contentParsed = BeautifulSoup(content.text, 'html.parser')
        imagesInContent = contentParsed.find_all('img')

        # print('contentParsed:\n', contentParsed)

        [images.append(image.get('src')) for image in imagesInContent if image.get('src') not in images]

        if imagesInContent:
            itemImages = []

            for image in imagesInContent:
                itemImages.append(urlparse.urlparse(image.get('src')))

            itemsWithImages[idx] = {
                'title': item.find('title').text,
                'images': itemImages,
            }

    print('-----------------------------------')

if images:

    images.sort()

    print('Number of images: ' + str(len(images)))

    if os.path.isfile(textFileName):
        os.remove(textFileName)

    with open(textFileName, 'w+') as f:

        f.write('Number of images: \n')

        for idx2, image in enumerate(images, 1):
            f.write(str(idx2) + ': ' + image + '\n')

        f.write('\nItems with images: \n')

        for key, value in itemsWithImages.items():
            f.write('Item ' + str(key) + ': \n' + str(value['title']) + '\n')
            f.write('-----------------------------------\n')
            for idx4, imageUrl in enumerate(value['images'], 1):
                f.write(str(idx4) + ' - ' + url2pathname(imageUrl.path) + '\n')

            f.write('\n')

        

    if os.path.isdir('images'):
        shutil.rmtree('images')

    os.mkdir('images')
    os.chdir('images')

    for image in images:
        imagePath = url2pathname(urlparse.urlparse(image).path)
        
        if os.path.dirname(imagePath):
            os.makedirs('.' + os.path.dirname(imagePath), exist_ok=True)
        download(image, '.' + imagePath)
        # time.sleep(1)

    os.chdir('../')

else:
    print('-----------------------------------')
    print('No images found.')
    print('-----------------------------------')

