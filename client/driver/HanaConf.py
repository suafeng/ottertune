#
# OtterTune - PostgresConf.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#
'''
Created on Sept 7, 2018
@author: Tao Dai
'''

import sys
import json
from collections import OrderedDict

# [execution]
# max_concurrency (indexserver.ini)
# default_statement_concurrency_limit (indexserver.ini)
#
# [sql]
# sql_executors (indexserver.ini)
#
# [memorymanager]
# statement_memory_limit (global.ini)

def main():
    if (len(sys.argv) != 3):
        raise Exception("Usage: python confparser.py [Next Config] [Current Config]")

    with open(sys.argv[1], "r") as f:
        conf = json.load(f,
                         encoding="UTF-8",
                         object_pairs_hook=OrderedDict)
    conf = conf['recommendation']
    # indexserver_knobs = {'sql_executors', 'max_concurrency', 'default_statement_concurrency_limit'}
    # second arg passed in as dir
    indexserver_sql_knobs = {'sql_executors', 'max_sql_executors', 'plan_cache_size'}
    indexserver_execution_knobs = {'max_concurrency', 'default_statement_concurrency_limit', 'num_cores'}
    global_memorymanager_knobs = {'statement_memory_limit'}
    global_persistence_knobs = {'log_backup_timeout_s', 'savepoint_interval_s', 'log_segment_size_mb', 'log_buffer_size_kb', 'log_buffer_count'}

    with open(sys.argv[2] + '/indexserver.ini', "r+") as hanaconf:
        lines = hanaconf.readlines()
        settings_idx = lines.index("# Add settings for extensions here\n")
        hanaconf.seek(0)
        hanaconf.truncate(0)

        lines = lines[0:(settings_idx + 1)]
        for line in lines:
            hanaconf.write(line)

        for (knob_name, knob_value) in list(conf.items()):
            if knob_name in indexserver_sql_knobs:
                hanaconf.write('[sql]\n')
            elif knob_name in indexserver_execution_knobs:
                hanaconf.write('[execution]\n')
            else:
                continue
            hanaconf.write(str(knob_name) + " = " + str(knob_value) + "\n")

    with open(sys.argv[2] + '/global.ini', "r+") as hanaconf:
        lines = hanaconf.readlines()
        settings_idx = lines.index("# Add settings for extensions here\n")
        hanaconf.seek(0)
        hanaconf.truncate(0)

        lines = lines[0:(settings_idx + 1)]
        for line in lines:
            hanaconf.write(line)

        for (knob_name, knob_value) in list(conf.items()):
            if knob_name in global_memorymanager_knobs:
                hanaconf.write('[memorymanager]\n')
            elif knob_name in global_persistence_knobs:
                hanaconf.write('[persistence]\n')
            else:
                continue
            hanaconf.write(str(knob_name) + " = " + str(knob_value) + "\n")

if __name__ == "__main__":
    main()
