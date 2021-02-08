@echo off
set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib

echo ^<head^> > .\release\log11083.html
echo ^<link rel="stylesheet" href="style.css"^> >> .\release\log11083.html
echo ^<title^>Logik - Leistungsmesser (11083)^</title^> >> .\release\log11083.html
echo ^<style^> >> .\release\log11083.html
echo body { background: none; } >> .\release\log11083.html
echo ^</style^> >> .\release\log11083.html
echo ^<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"^> >> .\release\log11083.html
echo ^</head^> >> .\release\log11083.html

@echo on

type .\README.md | C:\Python27\python -m markdown -x tables >> .\release\log11083.html


cd ..\..
C:\Python27\python generator.pyc "11083_Leistungsmesser" UTF-8

xcopy .\projects\11083_Leistungsmesser\src .\projects\11083_Leistungsmesser\release

@echo Done.

@pause