
# Results for running audiotoolbox-aiff-tester on macOS 14.4

~~~
> python3 toisto-runner.py -v tools/audiotoolbox-aiff-tester

Testing command: tools/audiotoolbox-aiff-tester
OK    : tests/aifc/aifc-channels-2-fl32.aifc
OK    : tests/aifc/aifc-channels-4.aifc
OK    : tests/aifc/aifc-chunk-fllr.aifc
OK    : tests/aifc/aifc-chunk-ssnd-before-comm-fver.aifc
OK    : tests/aifc/aifc-chunk-unknown-size-zero.aifc
OK    : tests/aifc/aifc-chunk-unknown.aifc
OK    : tests/aifc/aifc-samplerate-8912.75.aifc
OK    : tests/aifc/aifc-type-23ni.aifc
OK    : tests/aifc/aifc-type-fl32-nan-inf.aifc
OK    : tests/aifc/aifc-type-fl32-uppercase.aifc
OK    : tests/aifc/aifc-type-fl32-wide-range.aifc
OK    : tests/aifc/aifc-type-fl32.aifc
OK    : tests/aifc/aifc-type-fl64-nan-inf.aifc
OK    : tests/aifc/aifc-type-fl64-uppercase.aifc
OK    : tests/aifc/aifc-type-fl64-wide-range.aifc
OK    : tests/aifc/aifc-type-fl64.aifc
OK    : tests/aifc/aifc-type-in24.aifc
OK    : tests/aifc/aifc-type-in32.aifc
OK    : tests/aifc/aifc-type-none-samplesize-12.aifc
OK    : tests/aifc/aifc-type-none-samplesize-16.aifc
OK    : tests/aifc/aifc-type-none-samplesize-23.aifc
OK    : tests/aifc/aifc-type-none-samplesize-24.aifc
OK    : tests/aifc/aifc-type-none-samplesize-31.aifc
OK    : tests/aifc/aifc-type-none-samplesize-32.aifc
OK    : tests/aifc/aifc-type-none-samplesize-5.aifc
OK    : tests/aifc/aifc-type-none-samplesize-8.aifc
OK    : tests/aifc/aifc-type-raw-u8.aifc
OK    : tests/aifc/aifc-type-sowt.aifc
OK    : tests/aifc/aifc-type-twos.aifc
OK    : tests/aiff/aiff-channels-1.aiff
OK    : tests/aiff/aiff-channels-10.aiff
OK    : tests/aiff/aiff-channels-2-bei16.aiff
OK    : tests/aiff/aiff-channels-2.aiff
OK    : tests/aiff/aiff-channels-4.aiff
OK    : tests/aiff/aiff-chunk-aesd.aiff
 - unsupported: aesd

FAIL  : tests/aiff/aiff-chunk-anno-two.aiff
 - values differ for "anno", got: '['FirstAnno']', expected: '['FirstAnno', 'SecondAnno']'

OK    : tests/aiff/aiff-chunk-anno.aiff
OK    : tests/aiff/aiff-chunk-appl-two.aiff
 - unsupported: appl

OK    : tests/aiff/aiff-chunk-appl.aiff
 - unsupported: appl

OK    : tests/aiff/aiff-chunk-auth.aiff
OK    : tests/aiff/aiff-chunk-chan.aiff
OK    : tests/aiff/aiff-chunk-comments-one.aiff

FAIL  : tests/aiff/aiff-chunk-comments-ref-marker.aiff
 - value missing: comments

FAIL  : tests/aiff/aiff-chunk-comments-two.aiff
 - values differ for "comments", got: '[{'timeStamp': 0, 'marker': 0, 'text': 'Hello'}]', expected: '[{'timeStamp': 0, 'marker': 0, 'text': 'Hello'}, {'timeStamp': 3740546029, 'marker': 0, 'text': 'Text'}]'

OK    : tests/aiff/aiff-chunk-comments-zero.aiff
OK    : tests/aiff/aiff-chunk-copy.aiff
OK    : tests/aiff/aiff-chunk-fllr.aiff
OK    : tests/aiff/aiff-chunk-hash.aiff
 - unsupported: hash

OK    : tests/aiff/aiff-chunk-inst.aiff
 - unsupported: inst

OK    : tests/aiff/aiff-chunk-markers-zero.aiff
OK    : tests/aiff/aiff-chunk-markers.aiff
OK    : tests/aiff/aiff-chunk-midi-two.aiff
 - unsupported: midi

OK    : tests/aiff/aiff-chunk-midi.aiff
 - unsupported: midi

OK    : tests/aiff/aiff-chunk-name.aiff
OK    : tests/aiff/aiff-chunk-ssnd-before-comm.aiff
OK    : tests/aiff/aiff-chunk-ssnd-blocksize.aiff
OK    : tests/aiff/aiff-chunk-ssnd-missing.aiff
OK    : tests/aiff/aiff-chunk-ssnd-offset-blocksize.aiff
OK    : tests/aiff/aiff-chunk-ssnd-offset.aiff
OK    : tests/aiff/aiff-chunk-ssnd-samples-one.aiff
OK    : tests/aiff/aiff-chunk-ssnd-samples-zero.aiff
OK    : tests/aiff/aiff-chunk-ssnd-vs-sampleframes.aiff
OK    : tests/aiff/aiff-samplerate-0.01.aiff
OK    : tests/aiff/aiff-samplerate-1.aiff
OK    : tests/aiff/aiff-samplerate-11025.aiff
OK    : tests/aiff/aiff-samplerate-22050.aiff
OK    : tests/aiff/aiff-samplerate-2900000.aiff
OK    : tests/aiff/aiff-samplerate-384000.aiff
OK    : tests/aiff/aiff-samplerate-44100.aiff
OK    : tests/aiff/aiff-samplerate-5298.25.aiff
OK    : tests/aiff/aiff-samplesize-1.aiff
OK    : tests/aiff/aiff-samplesize-12.aiff
OK    : tests/aiff/aiff-samplesize-16.aiff
OK    : tests/aiff/aiff-samplesize-20.aiff
OK    : tests/aiff/aiff-samplesize-24.aiff
OK    : tests/aiff/aiff-samplesize-29.aiff
OK    : tests/aiff/aiff-samplesize-32.aiff
OK    : tests/aiff/aiff-samplesize-4.aiff
OK    : tests/aiff/aiff-samplesize-8.aiff
OK    : tests/compressed/compressed-alaw-ch1.aifc
OK    : tests/compressed/compressed-alaw-ch2.aifc

FAIL  : tests/compressed/compressed-alaw-uppercase.aifc
* ERROR: can't open file: tests/compressed/compressed-alaw-uppercase.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-dwvw-16bit.aifc
* ERROR: can't open file: tests/compressed/compressed-dwvw-16bit.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-dwvw-24bit.aifc
* ERROR: can't open file: tests/compressed/compressed-dwvw-24bit.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-g722-ch1.aifc
* ERROR: can't open file: tests/compressed/compressed-g722-ch1.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-g722-ch2.aifc
* ERROR: can't open file: tests/compressed/compressed-g722-ch2.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-g722-ch3.aifc
* ERROR: can't open file: tests/compressed/compressed-g722-ch3.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-gsm.aifc
* ERROR: can't open file: tests/compressed/compressed-gsm.aifc (fmt?)
 - process returned non-zero exit status: 255

OK    : tests/compressed/compressed-ima4-ch1.aifc
OK    : tests/compressed/compressed-ima4-ch2.aifc

FAIL  : tests/compressed/compressed-mac3-ch1.aifc
* ERROR: can't open file: tests/compressed/compressed-mac3-ch1.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-mac3-ch2.aifc
* ERROR: can't open file: tests/compressed/compressed-mac3-ch2.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-mac6-ch1.aifc
* ERROR: can't open file: tests/compressed/compressed-mac6-ch1.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-mac6-ch2.aifc
* ERROR: can't open file: tests/compressed/compressed-mac6-ch2.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-qclp.aifc
* ERROR: can't open file: tests/compressed/compressed-qclp.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-qdm2-ch1.aifc
* ERROR: can't open file: tests/compressed/compressed-qdm2-ch1.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-qdm2-ch2.aifc
* ERROR: can't open file: tests/compressed/compressed-qdm2-ch2.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-qdmc-ch1.aifc
* ERROR: can't open file: tests/compressed/compressed-qdmc-ch1.aifc (fmt?)
 - process returned non-zero exit status: 255

FAIL  : tests/compressed/compressed-qdmc-ch2.aifc
* ERROR: can't open file: tests/compressed/compressed-qdmc-ch2.aifc (fmt?)
 - process returned non-zero exit status: 255

OK    : tests/compressed/compressed-ulaw-ch1.aifc
OK    : tests/compressed/compressed-ulaw-ch2.aifc

FAIL  : tests/compressed/compressed-ulaw-uppercase.aifc
* ERROR: can't open file: tests/compressed/compressed-ulaw-uppercase.aifc (fmt?)
 - process returned non-zero exit status: 255

OK    : tests/exported/audacity-i8-id3.aiff
OK    : tests/exported/audacity-i8.aiff
OK    : tests/exported/audacity-ima-adpcm.aifc
OK    : tests/exported/ffmpeg-id3-cover-art.aiff
OK    : tests/exported/ffmpeg-id3.aiff
OK    : tests/exported/ffmpeg-metadata.aiff
OK    : tests/exported/finder-codec-sowt.aifc
OK    : tests/exported/garageband-16-bit.aiff
OK    : tests/exported/garageband-24-bit.aiff
OK    : tests/exported/garageband-cyclemarker.aiff
OK    : tests/exported/imovie.aiff
OK    : tests/exported/itunes-16bit-stereo.aiff
OK    : tests/exported/itunes-8bit-mono.aiff
OK    : tests/exported/motion.aifc
OK    : tests/exported/python3-alaw.aifc
OK    : tests/exported/python3-ulaw.aifc

FAIL  : tests/exported/quicktime5-alaw.aifc
* ERROR: Can't set app format
 - process returned non-zero exit status: 255

OK    : tests/exported/quicktime5-fl32.aifc
OK    : tests/exported/quicktime5-fl64.aifc
OK    : tests/exported/quicktime5-samplesize-16.aiff
OK    : tests/exported/quicktime5-samplesize-24.aiff
OK    : tests/exported/quicktime5-samplesize-32.aiff
OK    : tests/exported/quicktime5-samplesize-8.aiff

FAIL  : tests/exported/quicktime5-ulaw.aifc
* ERROR: Can't set app format
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-aifc-no-comm.aifc
* ERROR: can't open file: tests/invalid/invalid-aifc-no-comm.aifc (dta?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-aiff-no-comm.aiff
* ERROR: can't open file: tests/invalid/invalid-aiff-no-comm.aiff (dta?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-channels-0.aiff
* ERROR: can't open file: tests/invalid/invalid-channels-0.aiff (fmt?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-chunk-comm-short.aifc
* ERROR: can't open file: tests/invalid/invalid-chunk-comm-short.aifc (fmt?)
 - process returned non-zero exit status: 255

(OK)  : tests/invalid/invalid-chunk-id.aiff

(FAIL): tests/invalid/invalid-compression-type.aifc
* ERROR: can't open file: tests/invalid/invalid-compression-type.aifc (fmt?)
 - process returned non-zero exit status: 255

(OK)  : tests/invalid/invalid-double-comm-ssnd.aiff
(OK)  : tests/invalid/invalid-extra-garbage-at-end.aiff
(OK)  : tests/invalid/invalid-file-too-short.aiff
(OK)  : tests/invalid/invalid-fver-bad-value.aifc
(OK)  : tests/invalid/invalid-no-fver.aifc

(FAIL): tests/invalid/invalid-samplerate-0.aiff
* ERROR: can't open file: tests/invalid/invalid-samplerate-0.aiff (fmt?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-samplerate-inf.aiff
* ERROR: can't open file: tests/invalid/invalid-samplerate-inf.aiff (fmt?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-samplerate-nan.aiff
* ERROR: can't open file: tests/invalid/invalid-samplerate-nan.aiff (fmt?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-samplesize-0.aiff
* ERROR: can't open file: tests/invalid/invalid-samplesize-0.aiff (fmt?)
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-samplesize-33.aiff
* ERROR: Can't set app format
 - process returned non-zero exit status: 255

(FAIL): tests/invalid/invalid-ssnd-large-size.aiff
 - values differ for "samplesPerChannel", got: '65527', expected: '4411'
 - values differ for "endSamples", channel 0, index 0, got: 0, expected: 33

(OK)  : tests/invalid/unspecified-chunk-anno-non-ascii.aiff
(OK)  : tests/invalid/unspecified-chunk-auth-non-ascii.aiff
(OK)  : tests/invalid/unspecified-chunk-comments-non-ascii.aiff
(OK)  : tests/invalid/unspecified-chunk-copy-non-ascii.aiff
(OK)  : tests/invalid/unspecified-chunk-markers-non-ascii.aiff
(OK)  : tests/invalid/unspecified-chunk-name-non-ascii.aiff

Total 149: 104 passed, 22 failed, 23 invalid, 0 ignored.

~~~
