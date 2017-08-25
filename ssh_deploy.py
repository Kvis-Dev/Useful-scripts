import fnmatch
import subprocess
import os
import paramiko

# user config
import sys

IGNORE_FILE = '.gitignore'
IGNORE_LIST = ['.git/*', '.hg/*']

SSH_SERVER = 'google.com'
SSH_PORT = 100500
SSH_LOGIN = 'root'
SSH_PASS = 'strong_password123'

SSH_DEST_DIR = '/home/user/megafolser/im/am/cool'

# LOCAL config

CMD_MD5_TREE = "find -type f -exec md5sum '{}' \;"
ROOT = os.path.dirname(os.path.abspath(__file__))


def filter_ignore(filenames):
    global IGNORE_FILE, IGNORE_LIST

    with open(IGNORE_FILE, 'r') as f:
        ignore_files = [fn.strip() for fn in f.readlines() if fn] + IGNORE_LIST
        ignore_files = map(lambda x: x.split('#')[0], ignore_files)
        ignore_files = list(filter(len, [fn.strip() for fn in ignore_files]))

    for ignore in ignore_files:
        filenames = [n for n in filenames if not fnmatch.fnmatch(n, ignore)]

    return list(filter(len, filenames))


def exec(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out, err


cmd_local = "cd '" + ROOT + "' && " + CMD_MD5_TREE


def parse_output(f_sum):
    filenames_map = {}
    filenames = []

    for f in f_sum:
        # print(f)
        md5 = f[:32].strip()
        f_name = f[32:].strip()[2:]

        filenames.append(f_name)
        filenames_map[f_name] = md5

    return filenames, filenames_map


local_o, local_e = exec(cmd_local)
f_sum = local_o.decode('utf8').split('\n')

filenames, filenames_map = parse_output(f_sum)

# print('filenames_to_server')

filenames = filter_ignore(filenames)
# print(filenames)

# sys.exit(0)

s = paramiko.SSHClient()
s.load_system_host_keys()
s.connect(SSH_SERVER, SSH_PORT, SSH_LOGIN, SSH_PASS)
command = 'cd \'' + SSH_DEST_DIR + '\' && ' + CMD_MD5_TREE

stdin, stdout, stderr = s.exec_command(command)

filenames_server, filenames_map_server = parse_output(stdout.readlines())

# print('filenames_server')
# print(filenames_server, filenames_map_server)

to_send = []

for f_name in filenames:
    if f_name in filenames_map_server:
        if filenames_map_server[f_name] != filenames_map[f_name]:
            to_send.append(f_name)
    else:
        to_send.append(f_name)

print('to send:')
print(to_send)

if len(to_send):
    sftp = s.open_sftp()
    for f in to_send:
        localpath = ROOT + '/' + f
        remotepath = SSH_DEST_DIR + '/' + f
        print(localpath, '->', remotepath)
        sftp.put(localpath, remotepath)

    sftp.close()

s.close()
