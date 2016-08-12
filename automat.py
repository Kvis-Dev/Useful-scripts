#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import subprocess

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def main():
	path = '/home/user/webdev/'
	mod = False
	for subdirname in get_immediate_subdirectories(path):
		if (not os.path.exists("/etc/apache2/sites-available/" + subdirname+ ".conf") ):
			sitefile = open("/etc/apache2/sites-available/" + subdirname+ ".conf", "w")

			if os.path.isfile(os.path.join(path, subdirname, 'yii')):
				docrootdir = subdirname + '/web'
			else:
				docrootdir = subdirname

			sitefile.write("""<VirtualHost *:80>
ServerName """ + subdirname + """		
ServerAlias www.""" + subdirname + """		
DocumentRoot """ + os.path.join(path, docrootdir) + """
<Location />
  Require all granted
</Location> 
<Directory />
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
</Directory>
</VirtualHost>""")
			sitefile.close()
			print("Creating file /etc/apache2/sites-available/" + subdirname + ".conf");
			
			print('Writing to hosts file');
			hosts = open("/etc/hosts", "a")
			hosts.write("\n 127.0.0.1 " + subdirname)
			hosts.close()
		
			print('enabling site');
			os.system('a2ensite ' + subdirname)
			mod = True
		else:
			print subdirname + ' - Ok'
	
	
	print('Restarting apache');
	os.system('/etc/init.d/apache2 reload')
		
	return 0

if __name__ == '__main__':
	if os.getuid() == 0:
		main();
	else:
		print 'Need sudo'
		os.system('sudo ' +  os.path.abspath( __file__ ))
		
		
		

