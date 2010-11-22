Installation
============
Download the script as sendsms.py

First time run:
Run the script with the --setup argument
  $:	./sendsms.py --setup
The script will ask you your indyarocks.com username, password, and full name.
That's it! setup complete.

Usage
=====

*	To send an sms to a number 9812345678 type
	   	$:./sendsms.py 9812345678 "This message will be sent via SMS"

   	You may ommit the message part in the command line arguement. In that case, the script will prompt you to enter through standard input

		$:./sendsms.py 9812345678
		Reading Authfile:/home/user/.sendsms.auth
		Read!
		Please Enter the message( 140 chars only)
		This message will be sent via SMS
		I can give multiline messages too.
		Ctrl+D

	here Ctrl+D is the End-Of-File sequence (On Windows, it would be Ctrl+Z I think)

*	You can also specify your phonebook in the authfile (defualt is .sendsms.auth)
	Open the file .sendsms.auth
	In the [Phonebook] section, just enter the name=number values

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

*	You can also specify multiple recievers's seperated by a dot `.' to send the same message to more than one reciever.
	    	$./sendsms.py bill.9897949554.neo "This is a message"


Windows Users
=============
Windows users are required to install Python 2.x (that is any Python 2 version).
They need to use the command prompt with explicity Python program.
That is, instead of
     	      $: ./sendsms.py reciver message
They need to use
     	      $: python sendsms.py reciever message
Example
	      > python sendsms.py bill "HI Bill"

You might also need to add Python to your system path. You can do this by typing the following command in your command line (invoked by cmd.exe)
    	      path = %PATH%;C:\Python27\
where C:\Python27 is the place where your Python is installed
-------------------------------------------------------------------
    
