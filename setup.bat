@echo off
setlocal

rem 사용자에게 아이디를 물어본다
set /p username="ID: "

rem 서버 정보 설정
set hostname=
set port=

rem 현재 경로를 변수에 저장
set current_dir=%cd%

scp -P $port% -r %username%@%hostname%:/opt/XXX %current_dir%\backend
scp -P $port% %username%@%hostname%:/opt/XXX.json %current_dir%\backend\XXX.json

echo Done!
endlocal
