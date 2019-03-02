### PYLOC
Python implementation of tool for counting lines of code.

#### Usage
pyloc --help
```
usage: pyloc [options]

positional arguments:
  path              working directory

optional arguments:
  -h, --help        show this help message and exit
  -gi, --gitignore  filter sources by .gitignore file

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
