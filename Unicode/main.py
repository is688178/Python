"""
Propiedades Unicode
"""
import unicodedata

u = chr(233) + chr(0x0bf2) + chr(3972) + chr(6000) + chr(13231)

for i, c in enumerate(u):
    print(i, '%04x' % ord(c), unicodedata.category(c), end=" ")
    print(unicodedata.name(c))

# Get numeric value of second character
print(unicodedata.numeric(u[1]))

"""
Expresiones regulares Unicode
"""
import re
p = re.compile(r'\d+')

s = "Over \u0e55\u0e57 57 flavours"
m = p.search(s)
print(repr(m.group()))

s = "Over 57 flavours"
m = p.search(s)
print(repr(m.group()))

"""
Leyendo y escribiendo datos Unicode
"""
with open('unicode.txt', encoding='utf-8', mode='w+') as f:
    f.write('\u4500 blah blah blah\n')
    f.seek(0)
    print(repr(f.readline()[:1]))

with open('unicode.txt', encoding='utf-8') as f:
    for line in f:
        print(repr(line))
