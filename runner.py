
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
    ch = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    res = ch.communicate()
    return (res[0], res[1], ch.returncode)

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

def compare_samples(testref, testresult, fieldname, tolerance, errors):
    for chinx, chsamples in enumerate(testref[fieldname]):
        for inx, sample in enumerate(chsamples):
            if chinx < len(testresult[fieldname]) and inx < len(testresult[fieldname][chinx]):
                tres = testresult[fieldname][chinx][inx]
            else:
                tres = "none"
            if isinstance(tres, (int, float)) and isinstance(sample, (int, float)):
                # allow some variation in values, because of possible rounding errors
                if tres < sample-tolerance or tres > sample+tolerance:
                    errors.append(" - values differ for \"" + fieldname + "\", channel " + str(chinx) + ", index " + str(inx) + ", got: " + str(tres) + ", expected: " + str(sample))
                    return
            elif tres != sample:
                errors.append(" - values differ for \"" + fieldname + "\", channel " + str(chinx) + ", index " + str(inx) + ", got: " + str(tres) + ", expected: " + str(sample))
                return

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
needs_linefeed_before_ok = False

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
    (res, cmderror, exitstatus) = run_command(args["command"], aiff_filename, args["verbose"])
    if exitstatus != 0:
        print("\nFAIL: "+aiff_filename)
        if len(cmderror) > 0:
            print(cmderror.decode("utf-8").strip())
        print(" - process returned non-zero exit status: "+str(exitstatus))
        failcount += 1
        needs_linefeed_before_ok = True
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

    tolerance = 0
    if "tolerance" in testref:
        tolerance = float(testref["tolerance"])

    ck = check_key(testresult, testref, "startSamples")
    if ck != "":
        errors.append(ck)
    else:
        if testresult["startSamples"] != "-unsupported-":
            compare_samples(testref, testresult, "startSamples", tolerance, errors)
        else:
            errors.append(" - unsupported: startSamples");

    ck = check_key(testresult, testref, "endSamples")
    if ck != "":
        errors.append(ck)
    else:
        if testresult["endSamples"] != "-unsupported-":
            compare_samples(testref, testresult, "endSamples", tolerance, errors)
        else:
            errors.append(" - unsupported: endSamples");

    # unsupported error messages are not failures (except unsupported samples)
    failed = False
    for e in errors:
        if (e != "" and not e.startswith(" - unsupported")) or e == " - unsupported: startSamples" or e == " - unsupported: endSamples":
            failed = True
            break

    if failed:
        print("\nFAIL: "+aiff_filename)
        failcount += 1
        needs_linefeed_before_ok = True
    else:
        if needs_linefeed_before_ok:
            print("")
        needs_linefeed_before_ok = False
        print("OK  : "+aiff_filename)

    if len(cmderror) > 0:
        print(cmderror.decode("utf-8").strip())
        needs_linefeed_before_ok = True

    non_blank_errors = [e for e in errors if e != ""]
    errorstr = "\n".join(non_blank_errors)
    if errorstr != "":
        print(errorstr)
        needs_linefeed_before_ok = True

print("Total " + str(totalcount) + ": " + str(totalcount-failcount) +  " passed, " + str(failcount) +  " failed.")
