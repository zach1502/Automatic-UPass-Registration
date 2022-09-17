@echo off
cls
:start
echo RUNNING AUTO UPASS REGISTRATION
SET lastRan=0
SET month=%date:~4,2%
SET day=%date:~7,2%
IF %day% == 16 (
	IF NOT %month% == %lastRan% (
		python main.py
		SET lastRan=%date:~4,2%
	)
)
timeout /t 10000 /nobreak
goto start
