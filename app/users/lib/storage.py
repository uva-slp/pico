import os
import subprocess
from collections import namedtuple

from django.db import connection, OperationalError

from pico.secrets import DB_NAME
from pico.settings import BASE_DIR
from subprocess import CalledProcessError, check_output

# Path to containing git repository (if exists)
def git_root(path, default=BASE_DIR):
    try:
        return check_output('cd "%s" && git rev-parse --show-toplevel'%(path), shell=True).decode("utf-8").split('\n')[0]
    except CalledProcessError:
        return default
GIT_ROOT = git_root(BASE_DIR)

# Path to mountpoint
def mnt_root(path):
    return check_output('stat --format %%m "%s"'%(path), shell=True).decode("utf-8").split('\n')[0]
MNT_ROOT = mnt_root(BASE_DIR)

def disk_usage(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return namedtuple('usage', 'total used free')(total, used, free)

def du(path):
    return int(subprocess.check_output('du -sb "%s"'%(path), shell=True).split()[0].decode("utf-8"))

def usage_root():
    return disk_usage(MNT_ROOT)

def usage_pico():
    return du(GIT_ROOT)

def usage_db():
    try:
        cursor = connection.cursor(); cursor.execute(
            "SELECT sum( data_length + index_length ) " +
            "FROM information_schema.tables " +
            "WHERE table_schema=\"%s\";"%(DB_NAME)); return int(cursor.fetchone()[0])
    except OperationalError:
        # When information_schema.tables DNE (e.g. during testing)
        return 0
