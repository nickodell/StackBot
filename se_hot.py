import urllib2, re, config

def uniq(seq): 
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

def get_links():
    s = "http://stackexchange.com/questions?pagesize=50"
    h = urllib2.urlopen(s).read()
    l = re.findall('"((http)s?://.*?)"', h)
    l = map(lambda x: x[0], l)
    l = filter(lambda x: "/questions/" in x, l)
    l = filter(lambda x: "/tagged/" not in x, l)
    l = uniq(l)
    l = filter(lambda x: "/" + config.site_full + "/" in x, l)
    return l

def get_events():
    results = {}
    for link in get_links():
        question_num = re.search("\d+", link).group(0)
        results["se_" + config.site_short + "_" + question_num] = [
            "A question has appeared on the Hot Questions list:",
            link
        ]
    return results

