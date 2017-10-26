#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import subprocess

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def main():
	path = '/home/USER/webdev/'
	mod = False
	for subdirname in get_immediate_subdirectories(path):
		if (not os.path.exists("/etc/nginx/sites-enabled/" + subdirname+ "") ):
			sitefile = open("/etc/nginx/sites-enabled/" + subdirname+ "", "w")

			if os.path.isfile(os.path.join(path, subdirname, 'yii')):
				docrootdir = subdirname + '/web'
			else:
				docrootdir = subdirname

			print(subdirname);
			print(os.path.join(path, docrootdir));

			sitefile.write('''server {{
			    listen 80;
			    server_name {};

			    set $domain_path "{}";

			    root $domain_path;
			    index index.php index.html index.htm;

			    location / {{
			        try_files $uri $uri/ /index.php$is_args$args;
			    }}

			    location ~ \.php$ {{
			        include fastcgi_params;
			        fastcgi_param SCRIPT_FILENAME $domain_path$fastcgi_script_name;
			        fastcgi_pass unix:/run/php/php7.0-fpm.sock;
			        try_files $uri =404;
			    }}

			}}'''.format(
				subdirname,
				os.path.join(path, docrootdir),
				))


			sitefile.close()
			print("Creating file /etc/nginx/sites-enabled/" + subdirname + ".conf");
			
			print('Writing to hosts file');
			hosts = open("/etc/hosts", "a")
			hosts.write("\n127.0.0.1 " + subdirname)
			hosts.close()
		
			# print('enabling site');
			# os.system('a2ensite ' + subdirname)
			mod = True
		else:
			print (subdirname + ' - Ok')
	
	
	print('Restarting nginx');
	os.system('service nginx restart')
		
	return 0

if __name__ == '__main__':
	if os.getuid() == 0:
		main();
	else:
		print ('Need sudo')
		os.system('sudo ' +  os.path.abspath( __file__ ))
		
		
		
