## pyloc
[![](https://img.shields.io/badge/python-3.5+-blue.svg)]()

Python implementation of tool for counting lines of code.

### Installation
```
pip install -U git+https://github.com/reugn/pyloc.git
```

### Usage
pyloc --help
```
usage: pyloc [options]

positional arguments:
  path                  working directory

optional arguments:
  -h, --help            show this help message and exit
  -gi, --gitignore      filter sources by .gitignore file
  -s {files,comment,code,blank}, --sort {files,comment,code,blank}
                        sort results by field
  -o {table,json}, --out {table,json}
                        output format
```

Simple example
```
pyloc ./test
+------------+---------+-----------+--------+---------+
| File Ext   |   Files |   Comment |   Code |   Blank |
+============+=========+===========+========+=========+
| py         |       2 |       104 |    111 |      55 |
+------------+---------+-----------+--------+---------+
| c          |       1 |        24 |     70 |      21 |
+------------+---------+-----------+--------+---------+

```
