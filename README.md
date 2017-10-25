datam: data control
===================

`datam` supervises your data files.  It manages a list of files (the manifest)
along with their checksums.


Usage
-----
If you don't have a manifest file yet, you can start one.  Files can be added

```
datam add path1 path2
```

or removed:

```
datam pop
```

The local files can be verified against the manifest (by checksum):

```
datam verify
```

By default `datam` will store the manifest in a file called `manifest.json`.
A custom file may be specified with `--manifest path`

There is basic support for fetching data files from a remote source.  In this case the URL must be specified in the manifest file entry under the `remote` key.

```
datam clone
```

Dependencies
------------
`pyblake2`
`metafil`

Contributors
------------
Ben Granett


License
-------
MIT License

Copyright (c) 2017 Ben Granett

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
