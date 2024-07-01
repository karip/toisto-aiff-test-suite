
# Toisto AIFF Test Suite

This is an unofficial AIFF / AIFF-C audio file test suite.

## Usage

The `toisto-runner.py` script runs the test suite for the command given to it.

Here's examples running the test suite for macOS Audio ToolBox framework or
python aifc module. audiotoolbox-aiff-tester requires building it before running it.

    # for macOS
    cd tools
    clang++ ... # see audiotoolbox-aiff-tester.mm for compilation instructions
    cd ..
    python3 toisto-runner.py -v tools/audiotoolbox-aiff-tester
    # Total 152: 104 passed, 22 failed, 26 invalid, 0 ignored.

    # NOTE: install tinytag to test id3 tags
    python3 toisto-runner.py -v tools/python3-aiff-tester.py
    # Total 152: 75 passed, 51 failed, 26 invalid, 0 ignored.

[The results for Audio ToolBox framework](result-audiotoolbox-tester.md) running audiotoolbox-aiff-tester.

## Test cases

The test files are under the `tests` folder. They are valid AIFF/AIFF-C
audio files. The folder contains subfolders:

 - `aifc` - contains AIFF-C test files
 - `aiff` - contains AIFF test files
 - `compressed` - contains AIFF-C test files with compressed sample data
 - `exported` - contains test files exported from various apps
 - `invalid` - contains invalid AIFF and AIFF-C files

The `invalid` folder contains invalid files. The readers may or may not read them,
but hopefully they won't crash reading them. The unspecified files contain
non-ASCII characters in textual fields, which are not allowed by the spec.
However, macOS Audio Toolbox framework seems to read them as ISO 8859-1 or UTF-8.

## Expected results (json files)

Each audio file has a json file describing the expected result for reading
the audio file. The properties in the json file are:

 - `testinfo` - meta info about the test
   - `description` - short description of the test file
   - `notes` - additional notes about the test
   - `software` - name of the software used to create the file, if this is
                  missing, then the file was created manually in a hex editor
   - `version` - version of the software
   - `platform` - platform used to run the software ("macOS 12.4" / "Windows 7" ..)
   - `command` - command line tool and its arguments used to create the file

 - `result` - the test is a normal test if this is missing, `ignore` to ignore the test,
              `invalid` if the test file is an invalid file
 - `format` - format of the file: `aiff` or `aifc`
 - `sampleRate` - sample rate
 - `channels` - number of channels
 - `codec` - the compression type or type of uncompressed pcm sample data:
    `pcm_bei`=signed big-endian integer, `pcm_lei`=signed little-endian integer,
    `pcm_beu`=unsigned big-endian integer, `pcm_bef`=signed big-endian floating point
 - `sampleSize` - for uncompressed encodings, the sample size in bits 0-32 or 64, and
                  for compressed encodings, the decoded sample size (0 for variable sample size)
 - `markers` - a list of markers (the MARK chunk)
   - `id` - id of the marker
   - `position` - position of the marker
   - `name` - name of the marker
 - `comments` - a list of comments (the COMT chunk)
   - `timeStamp` - time stamp
   - `marker` - marker id
   - `text` - comment text
 - `inst` - the instrument chunk data with fields: `baseNote`, `detune`, `lowNote`, `highNote`,
    `lowVelocity`, `highVelocity`, `gain`, `sustainLoop` (`playMode`, `beginLoop`, `endLoop`),
    `releaseLoop` (`playMode`, `beginLoop`, `endLoop`)
 - `midi` - a list of a list of bytes in the MIDI chunks (multiple MIDI chunks are allowed)
 - `aesd` - a list of bytes in the AESD chunk
 - `appl` - a list of bytes in the APPL chunk
 - `name` - text of the NAME chunk
 - `auth` - text of the AUTH chunk
 - `(c)` - text of the (c) chunk
 - `anno` - a list of annotations (the ANNO chunks)
 - `id3` - id3 tags (the ID3 chunk)
 - `chan` - channel layout (the CHAN chunk) with fields: `channelLayoutTag`, `channelBitmap`,
    `channelDescriptions` (`label`, `flags`, `coordinates`)
 - `hash` - an array of 20 bytes containing the SHA-1 hash of the audio data
 - `samplesPerChannel` - the number of samples per channel after samples have been decoded
    (this may differ from the COMM chunk numSampleFrames value)
 - `tolerance` - how much sample values may differ from the expected values, default is 0
 - `startSamples` - a list of channels containing a list of samples (only the first 100-300 samples)
 - `endSamples` - a list of channels containing a list of samples (only the last 30 samples)

See [reftemplate.json](reftemplate.json) for examples for all the fields.

toisto-runner.py will compare each of these fields (except testinfo) against
the values returned by the command. If the fields match, the test passes.
If the command returns "-unsupported-", it means that the field is not
supported by the command and it won't affect the result of the test.

## Reference sample data

The `startSamples` and `endSamples` properties in the json file contain samples
for each channel. The range of values depends on `sampleSize`:

| Sample size |                Range                |
| :---------: | :---------------------------------: |
|    1..8     |             [-128, 127]             |
|    9..16    |           [-32768, 32767]           |
|   17..24    |         [-8388608, 8388607]         |
|   25..31    |      [-2147483648, 2147483647]      |
|     32      | [-2147483648, 2147483647] or floats |
|     64      |               floats                |

## Other test files

 - http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/AIFF/Samples.html

## References

 - [AIFF/AIFF-C Specifications](http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/AIFF/AIFF.html)
 - [Apple documentation about supported audio file formats in Mac OS X 10.5](https://developer.apple.com/library/archive/documentation/MusicAudio/Conceptual/CoreAudioOverview/SupportedAudioFormatsMacOSX/SupportedAudioFormatsMacOSX.html)
 - [wiki.multimedia.cx: ima4](https://wiki.multimedia.cx/index.php/Apple_QuickTime_IMA_ADPCM)
 - [wiki.multimedia.cx: Qclp](https://wiki.multimedia.cx/index.php/QCELP)
 - [wiki.multimedia.cx: QDesign Music Codec (QDMC / QDM2)](https://wiki.multimedia.cx/index.php/QDesign_Music_Codec)
 - [wiki.multimedia.cx: MAC3/MAC6](https://wiki.multimedia.cx/index.php/Apple_MACE)
 - [Apple comment about little-endian AIFF/AIFC files](https://lists.apple.com/archives/coreaudio-api/2009/Mar/msg00400.html)
 - [macOS Audio Toolbox framework](https://developer.apple.com/documentation/audiotoolbox/)
 - [Python3 AIFC module](https://docs.python.org/3/library/aifc.html)
 - [MIDI system exclusive message / Master Volume message](https://www.recordingblogs.com/wiki/midi-master-volume-message)

## License

All test files and source code is licensed under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
