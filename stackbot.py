import logging
import time
import sys
import chatexchange
import config

initted = False
def init():
    global client, me, room, initted
    print "Connecting to chat"
    logging.basicConfig(level=logging.DEBUG)

    client = chatexchange.Client('stackexchange.com', config.email, config.password)

    me = client.get_me()
    room = client.get_room(1549)
    initted = True
    print "init():", client, me, room

def send(text):
    print "sending: " + text
    if not initted:
        init()
    print "send():", client, me, room
    
    with room.new_messages() as messages:
        room.send_message(text)

        for message in messages:
            if message.owner is me:
                # Wait until you see a message from yourself
                # We might be in slow mode
                return

# The cache prevents the chatbot reposting things it has already submitted
# It gives each event a unique, unchanging id, like reddit_2rikav
def read_cache():
    try:
        cache = open("cache", "rt")
        cache = cache.read().strip()
    except:
        cache = ""
    cache = cache.split("\n")
    if "" in cache: cache.remove("")
    cache = map(lambda _str: _str.strip(), cache)
    return cache

def write_cache(cache):
    open("cache", "wt").write("\n".join(cache))

def get_all_events():
    events = {}
    import se_hot
    events = dict(events.items() + se_hot.get_events().items())
    import reddit_links
    events = dict(events.items() + reddit_links.get_events().items())
    return events

print "Stackbot running at " + time.strftime("%H:%M:%S")

silent = True
cache = read_cache()
events = get_all_events()
events = {event: detail for (event, detail) in
          events.iteritems() if event not in cache}

for event in events:
    for line in events[event]:
        silent = False
        send(line)
if not silent:
    send("Bot misbehaving? Ping @" + config.parent)
else:
    print "No work."
cache.extend(events.keys())
write_cache(cache)
