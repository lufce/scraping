import requests as webs
from lxml import etree
import os
from io import StringIO, BytesIO
from datashape.dispatch import namespace
import re

def webTest():
    req = webs.get("a")
    req.encoding = req.apparent_encoding
    print(req.text)

def environTest():
    url = 'http://jws.jalan.net/APIAdvance/HotelSearch/V1/?key={}&s_area=162612&count=2&xml_ptn=1' \
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

def getRatingFromHotelHTML():
    #設計を考えて
    hotel = open('my1.html', 'r')
    
    line = hotel.readline()
    
    while line:
        if re.match(r".*kuchikomi_spec_body_wrap.*", line):
            print(line)
            line = hotel.readline()
            break
        line = hotel.readline()

    while line:
        if re.match(r".*jlnpc-td05.*>(.+)</td>", line):
            m = re.match(r".*>(.+)</td>",line)
            print(line, end="")
            num = m.group(1)
            print(num.isnumeric())
            num2 = float(num)
            print(num2)
            print(type(num2))
            
        line = hotel.readline()
    
def test():
    s1 = "-"
    s2 = "3.2"
    
    try:
        float(s1)
        
    except ValueError:
        print('f1 is error')
        
    try:
        float(s2)
    
    except ValueError:
        print('f2 is error')
        
    print('end')
    
if __name__ == '__main__':
    test()
#     getRatingFromHotelHTML()