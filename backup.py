import time, os, datetime, sys, subprocess, glob


USER = 'root' #db user
PASSWORD = 'da pass'
DATABASE = 'database'
SKIP_TABLES = ['logs_users_request', 'sms']

DIRECTORY = '/home/user/backups'

todayDir = time.strftime("%d-%m-%Y")

if not os.path.exists("%s/%s" % (DIRECTORY, todayDir) ):
    os.makedirs("%s/%s" % (DIRECTORY, todayDir))
    print os.path.isdir("%s/%s" % (DIRECTORY, todayDir) )


IGN_TABLES = ''
for tbl in SKIP_TABLES:
	IGN_TABLES = IGN_TABLES + ' ' + '--ignore-table=%s.%s' % (DATABASE, tbl) 

TIME = time.strftime("%H-%M-%S")


oFile = '%s/%s/dump-%s.sql' % (DIRECTORY, todayDir, TIME)
backupString = "mysqldump -u %s -p%s%s %s > %s" % (USER, PASSWORD, IGN_TABLES, DATABASE, oFile)



yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
yesterday = yesterday.strftime("%d-%m-%Y")

print backupString

cmd = subprocess.Popen(backupString, shell=True, stdout=subprocess.PIPE).stdout.read()
cmd = subprocess.Popen("gzip " + oFile, shell=True, stdout=subprocess.PIPE).stdout.read()


yestFiles = glob.glob("%s/%s/*.sql.gz" % (DIRECTORY, yesterday) )
yestFilesList = {}

max = -1
for file in yestFiles:
    ltime = os.path.getmtime(file)
    yestFilesList[ ltime ] = file
    if ltime > max:
        max = ltime

for file in yestFiles:
    if not file == yestFilesList[max]:
        os.remove(file)

