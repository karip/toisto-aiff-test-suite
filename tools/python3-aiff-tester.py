#!/usr/bin/python3

# Tests how the python3 aifc package reads AIFF files.

import aifc
import sys
try:
    from tinytag import TinyTag
except ImportError:
    pass

try:
    afile = aifc.open(sys.argv[1], "r")
except Exception as e:
    print("Exception for '" + sys.argv[1] + "':", e, file=sys.stderr)
    exit(-1)

chcount = afile.getnchannels()
sampwidth = afile.getsampwidth()
samplerate = afile.getframerate()
comptype = afile.getcomptype().decode('utf-8')
if comptype == "NONE":
    comptype = "pcm_bei"
if comptype == "ALAW":
    comptype = "alaw"
if comptype == "ULAW":
    comptype = "ulaw"
compname = afile.getcompname()
markers = afile.getmarkers()
strframes = afile.readframes(1000000)
frames = []
for i in range(0, round(len(strframes)/sampwidth)):
    if sampwidth == 1:
        s = strframes[i]
        if s > 127:
            s -= 256
        frames.append(s)
    elif sampwidth == 2:
        if comptype == "alaw" or comptype == "ulaw" or comptype == "G722":
            s = strframes[i*2+1] * 256 + strframes[i*2]
        else:
            s = strframes[i*2] * 256 + strframes[i*2+1]
        if s > 32767:
            s -= 65536
        frames.append(s)
    elif sampwidth == 3:
        s = strframes[i*3] * 65536 + strframes[i*3+1] * 256 + strframes[i*3+2]
        if s > 8388607:
            s -= 16777216
        frames.append(s)
    elif sampwidth == 4:
        s = strframes[i*4] * 16777216 + strframes[i*4+1] * 65536 + strframes[i*4+2] * 256 + strframes[i*4+3]
        if s > 2147483647:
            s -= 4294967296
        frames.append(s)
afile.close()

print(f"{{")
print(f"    \"format\": \"-unsupported-\",")
print(f"    \"sampleRate\": {samplerate},")
print(f"    \"channels\": {chcount},")
print(f"    \"codec\": \"{comptype}\",")
print(f"    \"sampleSize\": {sampwidth*8},")

print(f"    \"chunks\": {{")

if markers:
    print(f"        \"markers\": [")
    m = []
    for marker in markers:
        m.append(f"            {{ \"id\": {marker[0]}, \"position\": {marker[1]}, \"name\": \"{marker[2].decode('utf-8')}\" }}")
    print(",\n".join(m))
    print(f"        ],")

if 'TinyTag' in vars():
    tag = TinyTag.get(sys.argv[1])
    print(f"        \"id3\": {{")
    tags = []
    if tag.artist:
        tags.append(f'            "ATT2": "{tag.title}"')
    if tag.artist:
        tags.append(f'            "TP1": "{tag.artist}"')
    if tag.album:
        tags.append(f'            "TAL": "{tag.album}"')
    if tag.track:
        if tag.track_total:
            tags.append(f'            "TRK": "{tag.track}/{tag.track_total}"')
        else:
            tags.append(f'            "TRK": "{tag.track}"')
    if tag.year:
        tags.append(f'            "TYE": "{tag.year}"')
    if tag.genre:
        tags.append(f'            "TCO": "{tag.genre}"')
    if tag.comment:
        tags.append(f'            "COM": "{tag.comment}"')
    print(",\n".join(tags))
    print(f"        }},")
else:
    print(f"        \"id3\": \"-unsupported-\",")

# TODO: implement writing out values for these if possible
print(f"        \"comments\": \"-unsupported-\",")
print(f"        \"inst\": \"-unsupported-\",")
print(f"        \"midi\": \"-unsupported-\",")
print(f"        \"aesd\": \"-unsupported-\",")
print(f"        \"appl\": \"-unsupported-\",")
print(f"        \"name\": \"-unsupported-\",")
print(f"        \"auth\": \"-unsupported-\",")
print(f"        \"(c)\": \"-unsupported-\",")
print(f"        \"anno\": \"-unsupported-\",")
print(f"        \"chan\": \"-unsupported-\",")
print(f"        \"hash\": \"-unsupported-\"")

print(f"    }},")   # end of chunks

samples_per_channel = int(len(frames)/chcount)
print(f"    \"samplesPerChannel\": {samples_per_channel},")

def print_samples(chcount, start, end, frames):
    for ch in range(0, chcount):
        print("        [ ", end='')
        valcnt = 0
        for pos in range(start, end):
            if pos != start:
                print(",", end='')
                valcnt += 1
                if (valcnt > 15):
                    valcnt = 0
                    print()
                    print("          ", end='')
                else:
                    print(" ", end='')
            print(frames[pos * chcount + ch], end='')
        if ch < chcount-1:
            print(" ],")
        else:
            print(" ]")

print(f"    \"startSamples\": [")
print_samples(chcount, 0, min(round(samples_per_channel), 300), frames)
print(f"    ],")

print(f"    \"endSamples\": [")
estart = samples_per_channel - 30
if estart < 0:
    estart = 0
print_samples(chcount, estart, samples_per_channel, frames)
print(f"    ]")

print(f"}}")
