Simple service to queue up entity objects (e.g. posts, comments) and create/update/delete
them in batch in an API endpoint. How the processing is orchestrated, e.g. sequentially or
 concurrently, is left up to separate classes that are loaded through dependency injection or
environment variables.

```
$ ./install.sh
New python executable in env/bin/python
Installing setuptools, pip...done.
Downloading/unpacking futures==3.0.4 (from -r requirements.txt (line 1))
  Downloading futures-3.0.4-py2-none-any.whl
Downloading/unpacking requests==2.9.1 (from -r requirements.txt (line 2))
  Downloading requests-2.9.1-py2.py3-none-any.whl (501kB): 501kB downloaded
Requirement already satisfied (use --upgrade to upgrade): wsgiref==0.1.2 in /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7 (from -r requirements.txt (line 3))
Installing collected packages: futures, requests
Successfully installed futures requests
Cleaning up...

Starting sequential mode...
Done - Execution time: 26.7892019749

Starting concurrent mode...
Done - Execution time: 18.7556169033
```
