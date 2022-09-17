# Automatic-UPass-Registration
Tired of registering for UPass every month? Good!
I present to you, a solution! (For Windows)
This script will automatically register for your upass when run.
However, if you have MFA enabled. Some user input is still required.

# How To Run?
I'm working on converting this python script into an .exe for ease of use for you, the user. 
But for now, I am assuming you have downloaded at least python 3.8

## Step 1.
Git clone this repo into your favourite folder! 
(or download the zip)

## Step 2.
Nice. Now double click the batch file inside this repo folder to run it.
Windows defender might complain but hey, feel free to read the code. I assure you it is safe.
Below, I break down the batch file code for you.

If you want to run it through cmd, you probably already know how to but write in
```start.bat```

## Step 3.
Now. Follow the script's instructions!

## Step 3b.
Asked to manually input browser?
Find your browser's shortcut (probably on your Desktop)

Right click, select `Open file location`.

![alt text](https://i.imgur.com/g1Z4rUx.png)

Click on the path above and copy paste it into the CMD window. APPEND THE EXE FILE TO THE END
![alt text](https://i.imgur.com/FLRlDWm.png)

E.g. I would be entering in `C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe`

# What does the Batchfile do?
A batchfile consists of a series of commands to be executed by a command line interpretter. For windows, it is cmd.

## Lines 1-3: Housekeeping
@echo off -> turns off showing the commands being run
cls -> CLear Screen
pip install -r requirements.txt -> download the dependancies to run the python script

## Lines 4-end: Conditional Checks
Run `python main.py` (the main python script) if and only if it is a new month and the day is greater than 16.
The condition will be checked every 10000 seconds. This will loop forever.


