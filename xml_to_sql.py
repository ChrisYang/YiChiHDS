#this is for parsing the xml file 
#it saves the results as a python dictionary 
#it is developed by Yizhi Zhang: yichi.zhang@wonga.com 
#All rights reserved 09/2014

import xml.etree.ElementTree as ET
#import xml2dict


class XmlListConfig(list):
    def __init__(self, aList):
        #print aList
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    #print element[0].tag
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                #print text
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        #print "here"
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                #print element
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                    #print element
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                    #print element
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
                #print element.text


def parse_dict(init, lkey=''):
    ret = {}
    for rkey,val in init.items():
        key = lkey+rkey
        if isinstance(val, dict):
            ret.update(parse_dict(val, key+'/'))
        else:
            #if 'pafvalid' in key:
                #print key,val
            ret[key] = val
    return ret

def addatwhere(d,string):
    dnew = {}
    for key,v in d.items():
        keys = key.split('/')
        if '</'+keys[-1]+'>' not in string:
            keys[-1] = '@'+keys[-1]
        key = '/'.join(keys)
        dnew[key] = v
    return dnew

def remove_xmlns(d,xmlns):
    dnew = {}
    for key,v in d.items():
        if xmlns in key:
            key = key.replace(xmlns, '')
        if 'accstartdate' in key:
            print key,v 
        dnew[key] = v
    return dnew

filename = "SerializedReport.xml"

with open (filename, "r") as myfile:
    string=myfile.read().replace('\n', '')
    
tree = ET.parse(filename)
root = tree.getroot()
xmldict = XmlDictConfig(root)
xmldict_flat = parse_dict(xmldict)
dictnew = remove_xmlns(xmldict_flat,'{urn:callcredit.co.uk/soap:bsbandcreditreport7}')

newdict = addatwhere(dictnew,string)

f =  open('allkey.sql','wb')
for key in newdict.keys():
    keys = key.split('/')
    combinedname = '_'.join(keys[-1:-4:-1])
    if '@' in combinedname:
        combinedname = combinedname.replace('@','')
    f.write( ''',CC.value('(//CallReportData/'''+ key+''')[1]','varchar(20)') as ''' +combinedname+'\n')
f.close()    

#print newdict.keys()
#print newdict
#print newdict.viewvalues()