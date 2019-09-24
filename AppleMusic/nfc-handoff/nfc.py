import spotipy.util
import os

if os.path.exists("dry-run"):

    idformat = "ClientID:"
    secretformat = "ClientSecret:"
    usernameformat = "Username:"

    memoryline = "";

    scopes = "user-read-currently-playing user-modify-playback-state user-read-playback-state streaming app-remote-control"
    url = "http://localhost/"

    with open('config.txt', 'r') as file:
        for line in file:
            if idformat in line:
                memoryline = line
                id = memoryline.rstrip(os.linesep)[11:][:-1]
            elif secretformat in line:
                memoryline = line
                secret = memoryline.rstrip(os.linesep)[15:][:-1]
            elif usernameformat in line:
                memoryline = line
                username = memoryline.rstrip(os.linesep)[11:][:-1]

    token = spotipy.util.prompt_for_user_token(username, scopes, id, secret, url)

    spotify = spotipy.Spotify(auth=token)

    songlist = spotify.search("test", 1, 0, "track", "DE")

else:
    path = os.path.realpath(__file__)
    os.remove(path[:-6] + "log.txt")

    timecodeformat = '"ssnc" "prgr":'
    songnameformat = "Title:"
    artistformat = "Artist:"
    idformat = "ClientID:"
    secretformat = "ClientSecret:"
    usernameformat = "Username:"
    deviceformat = "Device:"
    countryformat = "Country:"

    memoryline = "";
    timecodeline = "";

    scopes = "user-read-currently-playing user-modify-playback-state user-read-playback-state streaming app-remote-control"
    url = "http://localhost/"

    i = 3

    with open(path[:-6] + 'config.txt', 'r') as file:
        for line in file:
            if idformat in line:
                memoryline = line
                id = memoryline.rstrip(os.linesep)[11:][:-1]
            elif secretformat in line:
                memoryline = line
                secret = memoryline.rstrip(os.linesep)[15:][:-1]
            elif usernameformat in line:
                memoryline = line
                username = memoryline.rstrip(os.linesep)[11:][:-1]
            elif deviceformat in line:
                memoryline = line
                device = memoryline.rstrip(os.linesep)[9:][:-1]
            elif countryformat in line:
                memoryline = line
                country = memoryline.rstrip(os.linesep)[10:][:-1]

    with open(path[:-6] + 'airplay.txt', 'r') as file:
        for line in file:
            if timecodeformat in line:
                if i > 1:
                    i = i - 1
                else:
                    timecodeline = line
            elif songnameformat in line:
                memoryline = line
                songname = memoryline.rstrip(os.linesep)[8:][:-2]
            elif artistformat in line:
                memoryline = line
                artist = memoryline.rstrip(os.linesep)[9:][:-2]

    with open(path[:-6] + 'airplay2.txt', 'w') as file:
        file.write(timecodeline)

    timecodeline2 = timecodeline[16:]
    timecodeline3 = timecodeline2[:-3]

    timecodes = timecodeline3.split("/")
    starter = int(timecodes[0])
    mid = int(timecodes[1])
    end = int(timecodes[2])

    curr = round((mid - starter) / 44100)
    dur = round((end - starter) / 44100)

    if "feat." in songname:
        songname = songname.split("(")[0][:-1]

    with open(path[:-6] + 'log.txt', 'w') as file:
        file.write("Songname: " + songname + "\n"
                +   "Artist: " + artist + "\n"
                +   "Search for: " + songname + " " + artist + "\n"
                +  "Timecode 1: " + str(starter) + "\n"
                +  "Timecode 2: " + str(mid) + "\n"
                +  "Timecode 3: " + str(end) + "\n"
                +  "Timecode: " + timecodeline2 + "\n"
                +  "Curr: " + str(curr) + "\n"
                +  "Dur: " + str(dur))

    token = spotipy.util.prompt_for_user_token(username, scopes, id, secret, url)

    spotify = spotipy.Spotify(auth=token)

    songlist = spotify.search(songname + " " + artist, 1, 0, "track", country)

    song = songlist['tracks']['items'][0]['uri']

    spotify.start_playback(device, None, [song], None)
    spotify.seek_track(int(curr) * 1000, device)

    os.remove(path[:-6] + "airplay.txt")
    os.remove(path[:-6] + "airplay2.txt")