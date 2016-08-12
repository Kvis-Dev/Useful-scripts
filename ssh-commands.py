#!/usr/bin/python

import paramiko
import os
import datetime
import sys

HOST = 'somehost.com';
LOGIN = 'root'
PASS = 'pass'

BBUSER = 'Login'
BBPASS = 'Pass'


COMMANDS = []

if len(BBUSER) < 1:
	print ("No user specified!")
	sys.exit()

if len(BBPASS) < 1:
	BBPASS = input("Please enter your password: ")

UP = [
	{
	"name" : "Conname AI",
	"commands" : [" cd /home/selly/ai && hg pull https://" + BBUSER + ":" + BBPASS + "@bitbucket.org/User/sellyai && hg up -C && python3 console.py migrate && python3 console.py commands && python3 console.py self-teach && kill -9 `pgrep selly-ai-dbg`"]
	}
]

for site in UP:
	update = input("Want to update " + site['name'] + "[y/N]: ")
	if ( len(update) == 1 and update.lower() == 'y'):
		COMMANDS = COMMANDS + site['commands']


print( "Connecting through SSH" )
ssh    = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=LOGIN, password=PASS)
print( "Ok" )
print( "-" * 40 )

for cmd in COMMANDS:
	print( "Running command:", cmd )
	stdin, stdout, stderr = ssh.exec_command(cmd)
	stdin.flush()
	response = stdout.readlines()
	print( "RESPONSE:" )
	print( "\n".join(response) )
	print( "-" * 40 )

ssh.close()
