
# Creates AIFF files using python's aifc package.

import aifc
import argparse
import math
import sys

# documentation: https://docs.python.org/3/library/aifc.html

parser = argparse.ArgumentParser(description='Generates an aiff/aifc file.')
parser.add_argument('-f', '--format', type=str, help='format ("AIFF"/"AIFC")', default="AIFF")
parser.add_argument('-d', '--codec', type=str, help='codec (""/"ulaw"/"alaw"/"G722")', default="")
parser.add_argument('-b', '--bits', type=int, help='sample width in bits (16/8/24/32)', default=16)
parser.add_argument('-r', '--samplerate', type=int, help='sample rate (44100/11025/..)', default=44100)
parser.add_argument('-c', '--channels', type=int, help='number of channels (1/2/4/..)', default=2)
parser.add_argument('--freq', type=int, help='frequency of the sound in Hz (440/880/..)', default=440)
parser.add_argument('--dur', type=int, help='duration of the sound in ms (100/500/..)', default=100)
parser.add_argument('--markers', type=str, nargs='+', help='markers ("pos,name")', default="")
parser.add_argument('output', type=str, help='output filename')
args = parser.parse_args()

afile = aifc.open(args.output, "w")

# set parameters

if args.format == "AIFC":
    afile.aifc()
else:
    afile.aiff()
afile.setnchannels(args.channels)
afile.setframerate(args.samplerate)
samplebytes = math.ceil(args.bits / 8)
afile.setsampwidth(math.ceil(samplebytes))
if args.codec != "":
    names = {
        "ulaw": "Python compressed u-Law 2:1",
        "alaw": "Python compressed A-Law 2:1",
        "ULAW": "Python compressed ULAW",
        "ALAW": "Python compressed ALAW",
        "G722": "Python compressed G722"
    }
    afile.setcomptype(args.codec.encode("utf-8"), names[args.codec].encode("utf-8"))

# set markers

for index, marker in enumerate(args.markers):
    mvals = marker.split(",")
    afile.setmark(index+1, int(mvals[0]), mvals[1].encode("utf-8"))

# create the waveform as a byte string

total_len = math.ceil(args.dur * args.samplerate / 1000)

data = []

# add channel indicator (10, 20, ..)

SIG_SAMPLECOUNT = 8
for i in range(0, args.channels*SIG_SAMPLECOUNT):
    for ch in range(0, args.channels):
        if i >= ch*SIG_SAMPLECOUNT and i < ch*SIG_SAMPLECOUNT + SIG_SAMPLECOUNT:
            data.append(10 * (ch+1))
        else:
            data.append(0)

# add saw wave

amplitude = math.pow(2, args.bits) - 1
wavelen = args.samplerate / args.freq
CHANNELSHIFT = 8
firstwave = True
for t in range(0, total_len - args.channels*SIG_SAMPLECOUNT):
    for ch in range(0, args.channels):
        ts = t - ch * CHANNELSHIFT
        tl = ts / wavelen
        wt = tl - math.floor(tl)
        sample = wt
        sample = sample * amplitude - math.floor(amplitude/2) - 1
        if ts < 0:
            sample = 0
        if ch == 0 and firstwave and t > args.channels: # ensure the first wave goes to the max value
            prevsample = data[-args.channels]
            if prevsample > sample:
                data[-args.channels] = math.floor(amplitude/2)
                firstwave = False
        data.append(sample)

datastr = b""
for d in data:
    if d < 0:
        d += amplitude + 1
    if args.codec == "":
        datastr += math.floor(d).to_bytes(samplebytes, byteorder='big')
    else: # compressed data is little endian
        datastr += math.floor(d).to_bytes(samplebytes, byteorder='little')

afile.writeframes(datastr)

afile.close()
