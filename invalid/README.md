
# Invalid files

This folder contains invalid AIFF files. They can be used to test how software
reading AIFF files reacts to them.

The unspeficied files contain non-ASCII characters, which are not allowed
by the spec. However, macOS Audio Toolbox API seems to read them as
ISO 8859-1 or UTF-8.
