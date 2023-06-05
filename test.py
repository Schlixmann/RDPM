import requests
import xml.etree.ElementTree as ET
from lxml import etree
from xml.sax.saxutils import escape

cpee_url =  f"https://cpee.org/flow/engine/14567/properties/description/"
frag_url = f"https://cpee.org/flow/engine/15344/properties/description/"
ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}


with open("output/test.xml", "r") as f:
    a = f.read()

a = etree.fromstring(a)
x = a.xpath(".//cpee1:*[@id]", namespaces=ns)[1]
#x = x.xpath(".//cpee1:call", namespaces=ns)
print((x.attrib["id"]))