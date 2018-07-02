import requests as webs
from lxml import etree
import os
from io import StringIO, BytesIO
from datashape.dispatch import namespace

def webTest():
    req = webs.get("a")
    req.encoding = req.apparent_encoding
    print(req.text)

def environTest():
    url = 'http://jws.jalan.net/APIAdvance/HotelSearch/V1/?key={}&s_area=162612&count=2&xml_ptn=3' \
        .format(os.environ['JALAN_KEY'])
    print(url)
    req = webs.get(url)
    req.encoding = req.apparent_encoding
    tree = etree.XML(req.content)
    output = open('my.xml', 'w')
    output.write(etree.tostring(tree).decode('UTF-8'))
    output.close()

def xmlTest():
    root = etree.parse('my.xml')
    print(type(root))
    tree = root.getroot()
    print(type(tree))
    
    hotel_url=''
    num = 1
    for e in tree.iter():
        if e.tag == '{jws}HotelDetailURL':
            hotel_url = e.text
    
            req = webs.get(hotel_url)
            req.encoding = req.apparent_encoding
            output = open('my{}.html'.format(num), 'w')
            output.write(req.text)
            output.close()
            num = num+1

if __name__ == '__main__':
    xmlTest()