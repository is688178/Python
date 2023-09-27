# Leyendo con xml.etree.ElementTree
import xml.etree.ElementTree as ET
import pandas as pd

xml_data = open('./properties.xml', 'r').read()  # Read file
root = ET.XML(xml_data)  # Parse XML

data = []
cols = []
for i, child in enumerate(root):
    data.append([subchild.text for subchild in child])
    cols.append(child.tag)

df = pd.DataFrame(data).T  # Write in DF and transpose it
df.columns = cols  # Update column names
print("Leyendo con xml.etree.ElementTree")
print(df)
print()

# Leyendo con lxml (Python binding for the C libraries libxml2 and libxslt)
# $ pip install lxml
from lxml import objectify

xml_data = objectify.parse('properties.xml')  # Parse XML data
root = xml_data.getroot()  # Root element

data = []
cols = []
for i in range(len(root.getchildren())):
    child = root.getchildren()[i]
    data.append([subchild.text for subchild in child.getchildren()])
    cols.append(child.tag)

df = pd.DataFrame(data).T  # Create DataFrame and transpose it
df.columns = cols  # Update column names
print("Leyendo con lxml")
print(df)
print()

# Leyendo con xmltodict
# $ pip install xmltodict
import xmltodict

xml_data = open('properties.xml', 'r').read()  # Read data
xmlDict = xmltodict.parse(xml_data)  # Parse XML

cols = xmlDict['root'].keys()
data = []

for i in xmlDict['root']:
    child = xmlDict['root'][i]
    data.append([child[subchild]['#text'] for subchild in child])

df = pd.DataFrame(data).T  # Create DataFrame and transpose it.
df.columns = cols
print("Leyendo con xmltodict")
print(df)
print()

# Escribiendo con pandas
df = pd.DataFrame([[1.3, 1.4, 5.2],
                   [2.6, 1.4, 4.6],
                   [2.1, 5.6, 4.6]],
                  columns=['A', 'B', 'C'],
                  index=['X', 'Y', 'Z'])

xml_data = ['<root>']
for column in df.columns:
    xml_data.append('<{}>'.format(column))  # Opening element tag
    for field in df.index:
        # writing sub-elements
        xml_data.append('<{0}>{1}</{0}>'.format(field, df[column][field]))
    xml_data.append('</{}>'.format(column))  # Closing element tag
xml_data.append('</root>')

with open('coordinates.xml', 'w') as f:  # Writing in XML file
    for line in xml_data:
        f.write(line)

# Escribiendo con ElementTree
df = pd.DataFrame([[1.3, 1.4, 5.2],
                   [2.6, 1.4, 4.6],
                   [2.1, 5.6, 4.6]],
                  columns=['A', 'B', 'C'],
                  index=['X', 'Y', 'Z'])
header = df.columns

root = ET.Element('root')  # Root element

for column in df.columns:
    entry = ET.SubElement(root, column)  # Adding element
    for row in df.index:
        schild = row
        child = ET.SubElement(entry, schild)  # Adding sub-element
        child.text = str(df[column][schild])

xml_data = ET.tostring(root)  # binary string
with open('coordinates2.xml', 'w') as f:  # Write in file as utf-8
    f.write(xml_data.decode('utf-8'))

# Escribiendo con lxml
from lxml import etree as et

root = et.Element('root')  # Create root element
df = pd.DataFrame([[1.3, 1.4, 5.2],
                   [2.6, 1.4, 4.6],
                   [2.1, 5.6, 4.6]],
                  columns=['A', 'B', 'C'],
                  index=['X', 'Y', 'Z'])

for column in df.columns:
    entry = et.SubElement(root, column)  # Writing element
    for row in df.index:
        schild = row
        child = et.SubElement(entry, schild)  # Writing sub-elements
        child.text = str(df[column][schild])

xml_data = et.tostring(root)  # binary string
with open('coordinates3.xml', 'w') as f:  # Write in XML file as utf-8
    f.write(xml_data.decode('utf-8'))
