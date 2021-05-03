import time, random, re, json
from string import Formatter
infile = open("streamloading.json",mode="r",encoding="utf-8")
strgroup = json.load(infile)
loadarray = strgroup.get("Loading",["ERROR"])
tiparray = strgroup.get("Tips",["ERROR"])
changetip = 0
dictionary_keyword = re.compile("\\{.*?\\}")
loadfile = open("stream-loading-text.txt",mode="w",encoding="utf-8")
tipfile = open("stream-loading-tip.txt",mode="w",encoding="utf-8")

def dictionarylookup(istr):
    start = 0
    keywords = [fname for _, fname, _, _ in Formatter().parse(istr) if fname]
    for keyword in keywords:
        arg = random.choice(strgroup.get(keyword,["ERROR"]))
        istr = istr.replace("{"+keyword+"}",arg)
        print("Replaced keyword {0} with {1}".format(keyword,arg))
    return istr

while True:
    loadfile.seek(0)
    loadfile.truncate(0)
    loadfile.write(dictionarylookup(random.choice(loadarray)))
    loadfile.flush()
    changetip-=1
    
    if changetip<=0:
        tipfile.seek(0)
        tipfile.truncate(0)
        tipfile.write("Tip: "+dictionarylookup(random.choice(tiparray)))
        tipfile.flush()
        changetip = random.randrange(3,10)
        
    time.sleep(random.randrange(3,10))