import urllib2, json, time, re, config

def get_reddit_links():
    s = "https://www.reddit.com/domain/" + config.site_full + "/.json"
    data = json.loads(urllib2.urlopen(s).read())
    children = data['data']['children']
    for child in children:
        if child['data']['created_utc'] > time.time() - 2*24*60*60:
            yield "http://www.reddit.com" + child['data']['permalink']

def get_events():
    results = {}
    try:
        links = list(get_reddit_links())
    except :
        # Reddit blocks us sometimes
        # C'est la vie
        return {}
    for link in links:
        reddit_link_id = re.search("comments/([a-z0-9]+)", link).group(1)
        results["reddit_" + reddit_link_id] = [
            "A link to your site has been posted on reddit:",
            link
        ]
    return results
