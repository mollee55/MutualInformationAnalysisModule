import urllib2

filedata = urllib2.urlopen('https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/dev/Biochemistry/compounds.tsv')
datatowrite = filedata.read()

with open('data/compounds.tsv', 'wb') as f:
    f.write(datatowrite)
