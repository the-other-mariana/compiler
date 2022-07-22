# Compiler

## Requirements

- Python 3.8

- PLY library by David Beazley

## Install PLY

PLY is a yacc implementation for python made by David Beazley.

1. Download PLY: https://www.dabeaz.com/ply/ply.html

    -  You will have a file named `ply-3.11.tar.gz`

2. Download Express Zip File Compression in order to unzip this file. 

3. Extract it to `C:\Users\<username>\Documents\ply-src`, let's say.

4. Open a terminal and go to the directory:

```
cd C:\Users\<username>\Documents\ply-src\ply-3.11.tar\ply-3.11
```

where `setup.py` is. 


5. Then type:

```
python setup.py install
```

6. On `C:\Users\<username>\Documents\ply-src\ply-3.11.tar\ply-3.11` copy the folder `ply` and paste it on your python install directory: in my case, `C:\Users\<username>\AppData\Local\Programs\Python\Python38`

7. Now you can import ply on your python files:

```python
import ply.lex as lex
```

## Run The Compiler

Open a terminal and type:

```
python main.py test3.up
```

where test3.up is the source file you want to compile.

## Test Cases

- There are 10 test cases:

    - Tests 1-5: error test cases, each of these contains a screen capture of what is wrong and what the .err file shows regarding the part that is wrong.

    - Tests 6-10: success test cases, each of these contain all 4 output files plus the source file: .up, .lex, .err and .eje files.
