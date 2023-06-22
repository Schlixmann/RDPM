require "typhoeus"
require "json"
require "systemu"

xml = File.read(File.join(__dir__,ARGV[0])) 

response = Typhoeus.post(
    "https://cpee.org/flow/start/",
    headers: {
      'Content-Type': 'text/xml',
      'Content-ID': 'xml'
    },
    body: xml
  )

  
systemu("xdg-open https://cpee.org/flow/edit.html?monitor=#{JSON.parse(response.response_body)['CPEE-INSTANCE-URL']}")

