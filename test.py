import requests
import xml.etree.ElementTree as ET
from lxml import etree
from xml.sax.saxutils import escape

cpee_url =  f"https://cpee.org/flow/engine/14567/properties/description/"
frag_url = f"https://cpee.org/flow/engine/15344/properties/description/"
ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}

# location
location =  "cpee felix instance"

# send get request and save response
r = requests.get(url = cpee_url)
r1 = requests.get(url = frag_url)
# parse xml:
root = etree.fromstring(r.content)

# create demo resources
frag_1 = etree.fromstring(r1.content)


frag_1 = etree.ElementTree(frag_1.getchildren()[0])
for n in frag_1.iter():
    print(n)