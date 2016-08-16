# Userful-scripts

*nginx/nginx_yii_conf*

Sample config for Yii2 simple project for nginx.

*automat.py*

This script adds and configures virtual hosts. Requires sudo.
_Edit `path` variable_

*clean-jira.py*

Cleans messages from JIRA from your email. You need to edit your login and password for gmail.
I haven't tested it with other email providers.
See: https://support.google.com/accounts/answer/185833?hl=en

*ssh-commands.py*

Runs ssh commands on your server

*backup.py*

Make backups of MySQL database, puts it into separate directory.
Makes N backup files per day (depends on how many times you run it), removes all files but the last from previous days' backup folders.
