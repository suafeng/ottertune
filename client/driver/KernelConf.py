#
# OtterTune - KernelConf.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#

import sys
import json
import subprocess as sp
from collections import OrderedDict


def main():
    if (len(sys.argv) != 3):
        raise Exception("Usage: python confparser.py [Next Config] [Current Config]")

    # get current mem size
    pgdata = '/var/lib/postgresql/10/main/postmaster.pid'
    pid = sp.check_output(['sudo', 'head', '-1', pgdata]).strip().decode('UTF-8')
    mem_size = sp.check_output(['grep', '^VmPeak', '/proc/' + pid + '/status']).decode('UTF-8').split()[1]
    nr_hugepages_100per = (int(mem_size) // 2048) + 3

    with open(sys.argv[1], "r") as f:
        conf = json.load(f,
                         encoding="UTF-8",
                         object_pairs_hook=OrderedDict)
    conf = conf['recommendation']
    with open(sys.argv[2], "r+") as postgresqlconf:
        lines = postgresqlconf.readlines()
        settings_idx = lines.index("# Add settings for extensions here\n")
        postgresqlconf.seek(0)
        postgresqlconf.truncate(0)

        lines = lines[0:(settings_idx + 1)]
        for line in lines:
            postgresqlconf.write(line)

        for (knob_name, knob_value) in list(conf.items()):
            if 'vm.' in knob_name or 'kernel.' in knob_name:
                if knob_name == 'vm.nr_hugepages':
                    # continue
                    knob_value = int(nr_hugepages_100per * (int(knob_value) / 100)) + 1
                    if knob_value < 5000:
                        knob_value = 5000
                    sp.check_output(['sudo', 'sysctl', '-w', knob_name + '=' + str(knob_value)])
                # if knob_name == 'vm.overcommit_ratio' and int(str(knob_value)) < 75:

                print(sp.check_output(['sudo', 'sysctl', '-w', knob_name + '=' + str(knob_value)]))
            else:
                if str(knob_value) == '0B':
                    knob_value = '0'
                if 'B' in str(knob_value) and 'k' not in str(knob_value) and 'G' not in str(knob_value) and 'M' not in str(knob_value) and 'T' not in str(knob_value):
                    if str(knob_value)[:-1] == '-1': 
                        knob_value = '-1'
                    else: 
                        knob_value = '0'
                postgresqlconf.write(str(knob_name) + " = " + str(knob_value) + "\n")


if __name__ == "__main__":
    main()
