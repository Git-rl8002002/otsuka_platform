@echo off
cls
echo.
echo Choose one of the following operations:
echo 1 - Add netsh firewall block Facebook , IG , TikTok
echo 2 - Add netsh firewall block Facebook , IG , TikTok , Youtube
echo 3 - Del netsh firewall all rule 
echo 4 - Exit
choice /C 1234 /N /M "Select your option:"

echo.
if errorlevel 4 goto :EXIT
if errorlevel 3 goto :CMD
if errorlevel 2 goto :CALC
if errorlevel 1 goto :NOTEPAD

:NOTEPAD
echo Add netsh firewall block Facebook , IG , TikTok...
start notepad
    :::::::::::::::::::::::::::::::::::::::::::::
    ::
    :: block facebook , IG , tiktok , youtube
    ::
    :::::::::::::::::::::::::::::::::::::::::::::
    netsh advfirewall firewall add rule name="Block Facebook" dir=out action=block remoteip=31.13.87.0/24,157.240.11.0/24
    netsh advfirewall firewall add rule name="Block IG" dir=out action=block remoteip=31.13.87.0/24,157.240.11.174/24
    
    :: Tiktok ip : 173.222.248.0/24 , 199.59.243.225
    netsh advfirewall firewall add rule name="Block TikTok" dir=out action=block remoteip=13.35.166.0/24,23.195.89.0/24,23.195.91.0/24,23.195.90.0/24,173.222.248.0/24,96.7.229.0/24,199.59.243.0/24

    :: Youtube tw ip : 142.251.42.238,172.217.163.46,142.251.43.14,172.217.160.78
    ::netsh advfirewall firewall add rule name="Block Youtube" dir=out action=block remoteip=142.251.42.238,172.217.163.46,142.251.43.14


    :: google.com.tw ip : 172.217.160.99

goto :EOF

:CALC
echo Add netsh firewall block Facebook , IG , TikTok , Youtube...
start calc
    :::::::::::::::::::::::::::::::::::::::::::::
    ::
    :: block facebook , IG , tiktok , youtube
    ::
    :::::::::::::::::::::::::::::::::::::::::::::
    netsh advfirewall firewall add rule name="Block Facebook" dir=out action=block remoteip=31.13.87.0/24,157.240.11.0/24
    
    netsh advfirewall firewall add rule name="Block IG" dir=out action=block remoteip=31.13.87.0/24,157.240.11.174/24
    
    :: Tiktok ip : 173.222.248.0/24 , 199.59.243.225
    netsh advfirewall firewall add rule name="Block TikTok" dir=out action=block remoteip=13.35.166.0/24,23.195.89.0/24,23.195.91.0/24,23.195.90.0/24,173.222.248.0/24,96.7.229.0/24,199.59.243.0/24

    :: Youtube tw ip : 
    :: 142.251.42.238 , 172.217.163.46 , 142.251.43.14 , 172.217.160.78
    netsh advfirewall firewall add rule name="Block Youtube" dir=out action=block remoteip=172.217.160.110,142.251.43.14,142.251.42.238,172.217.163.46
    
    
    
    :: doc.google.com.tw  : 142.251.42.238
    :: google.com.tw      : 172.217.160.99
    :: bsignin.104.com.tw : 13.35.166.23, 13.35.166.3   , 13.35.166.54 , 13.35.166.111
    :: bsignin.104.com.tw : 3.164.110.8 , 3.164.110.112 , 3.164.110.93 , 3.164.110.88
goto :EOF

:CMD
echo Del netsh firewall all rule...
start cmd
    :::::::::::::::::::::::::::::::::::::::::::
    ::
    :: open facebook , IG , tiktok , youtube
    ::
    :::::::::::::::::::::::::::::::::::::::::::
    netsh advfirewall firewall delete rule name="Block Facebook"
    netsh advfirewall firewall delete rule name="Block IG"
    netsh advfirewall firewall delete rule name="Block TikTok"
    netsh advfirewall firewall delete rule name="Block Youtube"
goto :EOF

:EXIT
echo Exiting...
goto :EOF

:EOF
echo Operation completed.
pause

:::::::::::::::::::::::
::
:: show all firewall
::
:::::::::::::::::::::::
::netsh advfirewall show currentprofile
::netsh advfirewall firewall show rule name=all

:::::::::::::::::::::::::::::::::::::::::::::
::
:: block facebook , IG , tiktok , youtube
::
:::::::::::::::::::::::::::::::::::::::::::::
::netsh advfirewall firewall add rule name="Block Facebook" dir=out action=block remoteip=31.13.87.0/18,157.240.11.0/18
::netsh advfirewall firewall add rule name="Block IG" dir=out action=block remoteip=31.13.87.0/18,157.240.11.174/18
::netsh advfirewall firewall add rule name="Block TikTok" dir=out action=block remoteip=13.35.166.0/18,23.195.89.0/18,23.195.91.0/18,23.195.90.0/18

:: Youtube tw ip : 142.251.42.238,172.217.163.46,142.251.43.14,172.217.160.78
::netsh advfirewall firewall add rule name="Block Youtube" dir=out action=block remoteip=142.251.43.0/18,142.251.42.0/18,172.217.163.0/18,172.217.160.78


:: google.com.tw ip : 172.217.160.99




:::::::::::::::::::::::::::::::::::::::::::
::
:: open facebook , IG , tiktok , youtube
::
:::::::::::::::::::::::::::::::::::::::::::
::netsh advfirewall firewall delete rule name="Block Facebook"
::netsh advfirewall firewall delete rule name="Block IG"
::netsh advfirewall firewall delete rule name="Block TikTok"
::netsh advfirewall firewall delete rule name="Block Youtube"

