
# Runner for the AIFF test suite
#
# Calls command-to-test for each test file under the tests folder and compares its
# output to the test file's json file.
# Compatible with python 2.6 and python 3.
#

import json
import sys
import os
import subprocess

def run_command(command, filename, verbose):
    cmd = command + " " + filename
    if verbose:
        print("Command: "+cmd)
    ch = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = ch.communicate()[0]
    return (result, ch.returncode)

def check_key(testresult, testref, key):
    if not key in testresult:
        return " - value missing: " + str(key)
    if not key in testref:
        return " - BAD REFERENCE FILE: value missing: " + str(key)
    return ""

def compare_value(resval, refval, key):
    if type(refval) is list:
        if len(resval) != len(refval):
            return " - values differ for \"" + key + "\", got: '" + str(resval) + "', expected: '" +str(refval)+"'"
        for i in range(0, len(refval)):
            err = compare_value(resval[i], refval[i], key)
            if err != "":
                return err
        return ""

    if type(refval) is dict:
        for k in refval.keys():
            err = compare_field(resval, refval, k)
            if err != "":
                return err
        return ""

    if ((type(refval) is str and resval != refval) or
        (type(refval) is int and float(resval) != float(refval)) or
        (type(refval) is float and float(resval) != float(refval))):
        return " - values differ for \"" + key + "\", got: '" + str(resval) + "', expected: '" +str(refval)+"'"
    return ""

def compare_field(testresult, testref, key):
    if not key in testref:
        return ""
    if not key in testresult:
        return " - value missing: " + str(key)
    if testresult[key] == "-unsupported-":
        return " - unsupported: " + str(key)
    resval = testresult[key]
    refval = testref[key]
    return compare_value(resval, refval, key)

# main

args = {
    "verbose": False
}
findex = 1
while findex < len(sys.argv):
    if sys.argv[findex] == "-v":
        args["verbose"] = True
        findex += 1
    elif sys.argv[findex] == "-i":
        args["input_folder"] = sys.argv[findex+1]
        findex += 2
    else:
        args["command"] = sys.argv[findex]
        findex += 1

if not "command" in args:
    print("Usage: runner.py [-v] [-i input_folder] command")
    exit(-1)

print("Testing command: " + args["command"])
if not os.path.exists(args["command"]):
    print("ERROR: Command does not exist!")
    exit(-1)

# get files
if "input_folder" in args:
    ifolder = args["input_folder"]
    if not ifolder.endswith("/"):
        ifolder += "/"
    filenames = [ifolder+f for f in os.listdir(ifolder)]
else:
    filenames = ["tests/aifc/"+f for f in os.listdir("tests/aifc")]
    filenames += ["tests/aiff/"+f for f in os.listdir("tests/aiff")]
    filenames += ["tests/compressed/"+f for f in os.listdir("tests/compressed")]
    filenames += ["tests/exported/"+f for f in os.listdir("tests/exported")]
filenames.sort()

totalcount = 0
failcount = 0

# process json files
for filename in filenames:
    if not filename.endswith(".json"):
        continue

    totalcount += 1
    json_filename = filename
    aiff_filename = filename[0:-5]+".aifc"
    if not os.path.exists(aiff_filename):
        aiff_filename = filename[0:-5]+".aiff"

    # read ref file
    f = open(json_filename, "r")
    refcontents = f.read()
    try:
        testref = json.loads(refcontents)
    except:
        print("* ERROR: INVALID JSON IN REF FILE:", json_filename)
        print(refcontents)
        raise

    # execute command for aiff file
    (res, exitstatus) = run_command(args["command"], aiff_filename, args["verbose"])
    if exitstatus != 0:
        print("FAIL: "+aiff_filename)
        print(" - process returned non-zero exit status: "+str(exitstatus))
        failcount += 1
        continue

    # some commands return extra text before json, so remove it
    splitted = res.split(b"\"format\"", 1)
    cmdres = res
    if len(splitted) > 1:
        cmdres = b"{ \"format\""+splitted[1]

    # parse json
    try:
        testresult = json.loads(cmdres)
    except:
        print("* ERROR: GOT INVALID JSON FOR " +aiff_filename+ ":\n" + cmdres.decode("utf-8"))
        raise

    # compare results

    errors = []
    if testresult["format"] != "-unsupported-":
        errors.append(compare_field(testresult, testref, "format"))
    errors.append(compare_field(testresult, testref, "sampleRate"))
    errors.append(compare_field(testresult, testref, "channels"))
    errors.append(compare_field(testresult, testref, "codec"))
    if "sampleSize" in testref and testref["sampleSize"] != 0:
        errors.append(compare_field(testresult, testref, "sampleSize"))

    errors.append(compare_field(testresult, testref, "markers"))
    errors.append(compare_field(testresult, testref, "comments"))

    errors.append(compare_field(testresult, testref, "inst"))
    errors.append(compare_field(testresult, testref, "midi"))
    errors.append(compare_field(testresult, testref, "aesd"))
    errors.append(compare_field(testresult, testref, "appl"))

    errors.append(compare_field(testresult, testref, "chan"))
    errors.append(compare_field(testresult, testref, "hash"))

    errors.append(compare_field(testresult, testref, "name"))
    errors.append(compare_field(testresult, testref, "auth"))
    errors.append(compare_field(testresult, testref, "(c)"))
    errors.append(compare_field(testresult, testref, "anno"))

    errors.append(compare_field(testresult, testref, "id3"))

    errors.append(compare_field(testresult, testref, "samplesPerChannel"))

    ck = check_key(testresult, testref, "startSamples")
    if ck != "":
        errors.append(ck)
    else:
        if testresult["startSamples"] != "-unsupported-":
            for chinx, chsamples in enumerate(testref["startSamples"]):
                for inx, sample in enumerate(chsamples):
                    if chinx < len(testresult["startSamples"]) and inx < len(testresult["startSamples"][chinx]):
                        tres = testresult["startSamples"][chinx][inx]
                    else:
                        tres = 0
                    if tres != sample:
                        errors.append(" - values differ for \"startSamples\", channel " + str(chinx) + ", index " + str(inx) + ", got: " + str(tres) + ", expected: " + str(sample))
                        break

    ck = check_key(testresult, testref, "endSamples")
    if ck != "":
        errors.append(ck)
    else:
        if testresult["endSamples"] != "-unsupported-":
            for chinx, chsamples in enumerate(testref["endSamples"]):
                for inx, sample in enumerate(chsamples):
                    if chinx < len(testresult["endSamples"]) and inx < len(testresult["endSamples"][chinx]):
                        tres = testresult["endSamples"][chinx][inx]
                    else:
                        tres = 0
                    if tres != sample:
                        errors.append(" - values differ for \"endSamples\", channel " + str(chinx) + ", index " + str(inx) + ", got: " + str(tres) + ", expected: " + str(sample))
                        break

    # unsupported error messages are not failures
    failed = False
    for e in errors:
        if e != "" and not e.startswith(" - unsupported"):
            failed = True
            break
    if failed:
        failcount += 1
        print("FAIL: "+aiff_filename)
    else:
        print("OK  : "+aiff_filename)
    non_blank_errors = [e for e in errors if e != ""]
    errorstr = "\n".join(non_blank_errors)
    if errorstr != "":
        print(errorstr)

print("Total " + str(totalcount) + ": " + str(totalcount-failcount) +  " passed, " + str(failcount) +  " failed.")
