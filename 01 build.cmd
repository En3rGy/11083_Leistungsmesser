@echo off

set PROJ_DIR=11083_Leistungsmesser
set MAN_FILE_NAME=log11083.html
set TITLE=Leistungsmesser (11083)

set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib

echo Generating Manual Page
echo ^<head^> > .\release\%MAN_FILE_NAME%
echo ^<link rel="stylesheet" href="style.css"^> >> .\release\%MAN_FILE_NAME%
echo ^<title^>Logik - %TITLE%^</title^> >> .\release\%MAN_FILE_NAME%
echo ^<style^> >> .\release\%MAN_FILE_NAME%
echo body { background: none; } >> .\release\%MAN_FILE_NAME%
echo ^</style^> >> .\release\%MAN_FILE_NAME%
echo ^<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"^> >> .\release\%MAN_FILE_NAME%
echo ^</head^> >> .\release\%MAN_FILE_NAME%

type .\README.md | C:\Python27\python -m markdown -x tables >> .\release\%MAN_FILE_NAME%

echo Generating HSL-MOdule
cd ..\..
echo on
C:\Python27\python generator.pyc "%PROJ_DIR%" UTF-8
echo off

echo Putting everything together
xcopy .\projects\%PROJ_DIR%\src .\projects\%PROJ_DIR%\release

@echo Done.

@pause