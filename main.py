#!/usr/bin/env python

import settings as s
import display_helper as disp
import arrow
import json
import subprocess
import os
import sys


def set_user():
    os.setgid(s.BACKUPPC_USER_GID)
    os.setuid(s.BACKUPPC_USER_UID)


def get_data():
    # output = subprocess.getoutput(s.BACKUPPC_DIR + "/bin/BackupPC_serverMesg status hosts") # Py3
    output = subprocess.check_output([s.BACKUPPC_DIR + '/bin/BackupPC_serverMesg', 'status', 'hosts'],
                                     preexec_fn=set_user())  # Py2
    if s.DEBUG:
        print('Raw output:', output)
    return output


def perl_to_json(perlString):
    # garbageChars = "();" # Py3
    garbageChars = "();\n"  # Py2
    new = "{" + perlString.strip(garbageChars).replace("=>", ":").replace("undef", "null") + "}"
    if s.DEBUG:
        print('Cleaned Perl structure:', new)
    return new


def parse_data(data):
    data = data[21:]
    if s.DEBUG:
        print('Perl data structure:', data)
    return json.loads(perl_to_json(data))


def has(dict, key):
    return \
        key is not None \
        and key in dict \
        and dict.get(key) != ''


def convert_timestamp_in_dict(dict, key):
    if s.DEBUG:
        print('Timestamp to convert:', dict.get(key))
    if not has(dict, key):
        return None
    return arrow.get(dict.get(key)).humanize(locale='it')


def translate(string):
    if s.DEBUG:
        print('String:', string)
    if string in s.TRANSLATIONS:
        return s.TRANSLATIONS.get(string)
    return string


def coalesce(obj, fallback):
    return fallback if obj is None else obj


def filter_data(data, host):
    host = data[host]
    res = {
        'startTime': convert_timestamp_in_dict(host, 'startTime'),
        'endTime': convert_timestamp_in_dict(host, 'endTime'),
        'lastGoodBackupTime': convert_timestamp_in_dict(host, 'lastGoodBackupTime'),
        'status': translate(host.get('state')),
        'type': translate(host.get('type')),
        'error': host.get('error'),
        'errorTime': convert_timestamp_in_dict(host, 'errorTime'),
        'reason': translate(host.get('reason'))
    }
    if s.DEBUG:
        print('Filtered data:', json.dumps(res, sort_keys=True, indent=4))
    return res


def get_info(host):
    data = parse_data(get_data())
    if s.DEBUG:
        print('JSON data:', json.dumps(data, sort_keys=True, indent=4))
    return filter_data(data, host)


def chunkstring(string, length):
    if s.DEBUG:
        print(string)
    if type(string) != 'Exceptions.OSError':
        return []
    return (str[i:length + i].strip() for i in range(0, len(str), length))


def get_error_message(obj):
    if not has(obj, 'errorTime') or obj['errorTime'] is None:
        return []
    res = ['Errore: ' + obj.get('errorTime')] + list(chunkstring(data.get('error'), 21))
    if s.DEBUG:
        print(res)
    return res


if __name__ == '__main__':
    disp.init()
    while True:
        try:
            data = get_info(s.TARGET_HOST)
            # print(json.dumps(data, sort_keys=True, indent=4))
            disp.show([
                          'Stato: ' + data['status'][0:14],
                          data['reason'] if data['status'] == 'inattivo' else data['status'][14:],
                          'Tipo: ' + data['type'],
                          'Ultimo: ' + coalesce(data['lastGoodBackupTime'], ''),
                      ] + get_error_message(data))
            # time.sleep(1)
        except:
            disp.show(['Errore script: '] + list(chunkstring(sys.exc_info()[0], 21)))
