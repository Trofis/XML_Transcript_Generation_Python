# file_meta = open('metadata.csv', 'r')
# Lines = file_meta.readlines()
 
# count = 0

# # Strips the newline character
# for line in Lines:
#     count += 1

import csv
from xml.etree.ElementTree import Element

#-------------------------------
#FILE
file_echange = open('files/XML_ESLO2_ENT_1054 _echange.csv')
file_enregistrement = open('files/XML_ESLO2_ENT_1054 _enregistrement.csv')
file_transcription = open('files/XML_ESLO2_ENT_1054 _transcription.csv')


csvreader_echange = csv.reader(file_echange)
csvreader_enregistrement = csv.reader(file_enregistrement)
csvreader_transcription = csv.reader(file_transcription)


#-------------------------------
# META : Enregistrement + Transcription

header_meta = []
header_meta  = next(csvreader_enregistrement,csvreader_transcription )[0].split(',,')


meta_all = []
for row in csvreader_enregistrement:
        meta_all.append(row)

for row in csvreader_transcription:
        meta_all.append(row)

meta = meta_all[1][0].split(';')

#-------------------------------
#DATA

header_data = []
header_data = next(csvreader_echange)[0].split(',')

data = []
for row in csvreader_echange:
        data.append(row[0].split(';'))



#--------------------------
#Write file

import xml.etree.cElementTree as ET
from xml.dom import minidom


root = ET.Element('FILMS')
count = 0

for elem in meta:
    ET.SubElement(root, header_meta[count]).text = meta[count]
    count +=1

turns = ET.SubElement(root,'dialogue')
current_turn = 0
sentence = 1
sentences_elem = None
for turn in data:
    count = 0
    for elem in turn:
        turnx = elem
        if count == 0:
            if current_turn != int(turnx):
                turn_elem = ET.SubElement(turns, "turn"+str(turnx))
                sentence = 1
                current_turn+=1
                ET.SubElement(turn_elem, header_data[count].replace(' ','_')).text = elem
                sentences_elem = ET.SubElement(turn_elem, "sentences")


            count +=1

            sentence_elem = ET.SubElement(sentences_elem, 'sentence'+str(sentence))
            sentence +=1
            continue

            
        ET.SubElement(sentence_elem, header_data[count].replace(' ','_')).text = elem
        
        count +=1
    


tree = ET.ElementTree(root)


#tree.write("filename.xml")
#print(ET.tostring(root, encoding='utf-8').decode())
xmlstr = minidom.parseString(ET.tostring(root, encoding='utf-8').decode()).toprettyxml(indent="   ")
with open("New_Database.xml", "w") as f:
    f.write(xmlstr)

print('ok')