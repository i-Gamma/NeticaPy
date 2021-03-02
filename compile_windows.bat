@ECHO OFF
CLS
IF %PROCESSOR_ARCHITECTURE% EQU x86  (copy Netica_API_504_windows\lib\32 bit\*.* Netica_API_504_windows\lib\) ELSE IF %PROCESSOR_ARCHITECTURE% EQU X86  (copy Netica_API_504_windows\lib\32bit\*.* Netica_API_504_windows\lib\) ElSE  (copy Netica_API_504_windows\lib\64bit\*.* Netica_API_504_windows\lib\)
set msvc=C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\
call "%msvc%vcvarsall.bat" %PROCESSOR_ARCHITECTURE%

cd Netica_API_504_windows\src
echo "Compiling NeticaEx.o"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29333\bin\Hostx64\x64\cl.exe" /c /I. NeticaEx.c /link ..\lib\Netica.lib
COPY *.obj ..\lib\
cd ..\..
copy Netica_API_504_windows\lib\Netica.dll
COPY Netica_API_504_windows\NeticaPy.pyx
echo compiling cython to c
cython -a NeticaPy.pyx
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29333\bin\Hostx64\x64\cl.exe"  /nologo /LD /W4  /INetica_API_504_windows\src\ /IC:\Anaconda3\include  /IC:\Anaconda3\PC /FeNeticaPy.pyd  /TcNeticaPy.c    /link Netica_API_504_windows\lib\NeticaEx  /link Netica_API_504_windows\lib\Netica.lib /dll  /libpath:C:\Anaconda3\libs 
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29333\bin\Hostx64\x64\cl.exe" /LD /W4   /D_USRDLL /D_WINDLL  /INetica_API_504_windows\src\ /IC:\Anaconda3\include  /IC:\Anaconda3\PC  /TcNeticaPy.c    /link Netica_API_504_windows\lib\NeticaEx  /link Netica_API_504_windows\lib\Netica.lib   /dll /libpath:C:\Anaconda3\libs /OUT:NeticaPy.dll

del *.c
del *.html
del *.pyx
del *.obj
del *.lib
del *.exe

echo "Done."
