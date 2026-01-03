@echo off
call "D:\Code\VS2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
python "E:\GitHub3\cpp\BPython\test\build_bpython.py" %*
