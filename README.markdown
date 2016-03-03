I no longer maintain this script. It seems that fullonsms.com has a captcha which would prevent this (or any such) script from working.
sendsms.py
=========
It is a small python script which act as a simple non-interactive front-end to the sms facility provided by fullonsms dot com. This allows message sending through terminal or even in bash scripts and other programs.

What does it do?
---------------
It will allow you to send free text message to any mobile in India from your terminal. The message will be of maximum 160 characters.

Requirement
----------
-	Python2.x
-	An account at fullonsms dot com
-	argparse.py if you are running Python 2.6 or below (You can get this file easily on the internet, just put it in the same directory as sendsms.py)

Installation
------------
Download the script as sendsms.py
Give it executable permission
     $:chmod +x sendsms.py

First time run:
Run the script with the `--setup` argument
    	        $:	./sendsms.py --setup
The script will ask you your fullonsms mobile number and password.
That's it! setup complete.

Usage
----

*	To send an sms to a number *9812345678* type
	   	$:./sendsms.py 9812345678 "This message will be sent via SMS"

   	You may omit the message part in the command line argument. In that case, the script will prompt you to enter through standard input

		$:./sendsms.py 9812345678
		Reading Authfile:/home/user/.sendsms.auth
		Read!
		Please Enter the message( 160 chars only)
		This message will be sent via SMS
		I can give multiline messages too.
		Ctrl+D

	here `Ctrl+D` is the End-Of-File sequence (On Windows, it would be `Ctrl+Z` I think)

*	You can also specify your phone book in the authfile (default is .sendsms.auth)
	Open the file `.sendsms.auth`
	In the `[Phonebook]` section, just enter the `name=number` values

	   	## .sendsms.auth
		##
		.
		.(rest of your file)
		.
		[Phonebok]
		bill = 9612345678
		peter = 9912345678
		suresh = 9512345678
		neo = 9012345678
		honey = 9812345678

	Save your file, and now you can use the name instead of number

	     	$:./sendsms.py bill "Hello Bill, how are you doing"

*	You can also specify multiple receivers separated by a dot `.` to send the same message to more than one receiver.
	    	$./sendsms.py bill.9897949554.neo "This is a message"


Windows Users
------------
Windows users are required to install Python 2.x (that is any Python 2 version).
They need to use the command prompt with explicit Python program.
That is, instead of
     $: ./sendsms.py receiver message
They need to use
     $: python sendsms.py receiver message
Example
     > python sendsms.py bill "HI Bill"

You might also need to add Python to your system `PATH`. You can do this by typing the following command in your command line (invoked by `cmd.exe`)
     path = %PATH%;C:\Python27\
where C:\Python27 is the place where your Python is installed

Getting an fullon dot com account
-------------------------------------
Getting account on fullonsms dot com is easy. If you have valid mobile phone number of India, you can register it with fullonsms dot com easily. They send a verification code on your mobile.
If you are changing your account settings in `sendsms.py`, please use the `--setup` option instead of directly changing the Authfile by hand.

What happened to indyarocks dot com script?
-------------------------------------------
It is still there but I won't develop on it any further. It is in the indyarocks branch.

DISCLAIMER
=========
The author of this script is in no way associated with fullonsms dot com. This script is for personal or educational use only. Any commercial use is forbidden. Author takes no responsibility whatsoever if this script is misused in any way. Also, there is no warranty of any kind with this script.


