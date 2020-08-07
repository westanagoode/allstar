import requests
import json
import re
import sys
import html

TARGET_PATH = sys.argv[1]
with open("api_key.txt") as y:
    API_KEY = y.read().strip()

def get_lyrics():
    with open("lyrics.txt") as y:
        lyrics = y.read()
    return lyrics

def get_most_recent_viddy():
    r = requests.get("https://www.googleapis.com/youtube/v3/search",params={
        "key": API_KEY,
        "channelId": "UCGaVdbSav8xWuFWTadK6loA",
        "part": "snippet,id",
        "order": "date",
        "maxResults": 1,
        "type": "video",
    })
    d = json.loads(r.text)
    video_id = d["items"][0]["id"]["videoId"]
    title = d["items"][0]["snippet"]["title"]
    return [video_id,title]

def set_viddys(lst):
    with open("viddys.json","w") as y:
        y.write(json.dumps(lst))

def get_viddys():
    most_recent = get_most_recent_viddy()
    with open("viddys.json") as y:
        history = json.load(y)
    if most_recent != history[0]:
        history.insert(0,most_recent)
        set_viddys(history)
    return history

replacements = {
    "LOOKIN' KINDA DUMB": "LOOKING KIND OF DUMB",
    "THE METEOR MEN BEG TO DIFFER // JUDGING BY THE HOLE IN THE SATELLITE PICTURE": "THE METEOR MEN BEG TO DIFFER\nJUDGING BY THE HOLE IN THE SATELLITE PICTURE",
}

if __name__ == "__main__":

    viddys = get_viddys()

    lyrics = get_lyrics().upper()

    for video_id,video_title in get_viddys():
        video_title = html.unescape(video_title).upper().strip("!. ")
        if video_title == "OLD":
            continue
        if video_title in replacements:
            video_title = replacements[video_title]
        if video_title in lyrics:
            lyrics = lyrics.replace(
                video_title,
                "<a target='_blank' href='https://www.youtube.com/watch?v=%s'>%s</a>" % (video_id,video_title)
            )

    html = """
<!DOCTYPE html>
<html>
<head>
    <title>All Star Vlogbrothers</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    %s
</body>
</html>
    """ % lyrics.replace("IN THE SHAPE","\nIN THE SHAPE").replace("\n","<br/>")

    with open(TARGET_PATH,"w") as y:
        print(html,file=y)
