import requests
import json
import os
import sys


print(sys.argv)
xml = open(os.getcwd() +"/" + str(sys.argv[1])).read() 


response = requests.post(
    url = "https://cpee.org/flow/start/",
    headers= {
      'Content-Type': 'text/xml',
      'Content-ID': 'xml'
    },
    data = xml
  )
print(json.loads(response.content))
  
os.system(f"xdg-open https://cpee.org/flow/edit.html?monitor={json.loads(response.content)['CPEE-INSTANCE-URL']}")
