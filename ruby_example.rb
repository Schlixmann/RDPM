require 'xml/smart'
require 'typhoeus'

def get_allresources(resourceurl)
    res = Typhoeus.get resourceurl
    doc = XML::Smart.string(res.body)
     
    init_measure_dict = doc.find('//measures/*').map do |e|
      [e.qname.name, e.text.to_f]
    end.to_h

    doc.find('//resource').map do |e|
       res = new Resource(e.attributs['name'])
       changepatterns = e.find('resprofile/changepattern')
       measure_dict = init_measure_dict.merge(e.find('resprofile/measures/*').map do |m|
         [e.qname.name, e.text.to_f]
       end.to_h)
       res
    end
end    