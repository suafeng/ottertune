import sys
import subprocess as sp
import glob
import json
from collections import OrderedDict


def main():
    if (len(sys.argv) != 2):
        raise Exception("Usage: python add_kernel_knobs.py [Output Directory]")
    outputDir = sys.argv[1]

    # get current mem size
    pgdata = '/var/lib/postgresql/10/main/postmaster.pid'
    pid = sp.check_output(['sudo', 'head', '-1', pgdata]).strip().decode('UTF-8')
    mem_size = sp.check_output(['grep', '^VmPeak', '/proc/' + pid + '/status']).decode('UTF-8').split()[1]
    nr_hugepages_100per = (int(mem_size) // 2048) + 3

    # note not all of them are tunable, these are knobs shown on the website
    kernel_knobs = ['vm.swappiness', 'vm.overcommit_memory', 'vm.overcommit_ratio', 'vm.dirty_ratio',
                    'vm.dirty_bytes', 'vm.dirty_background_ratio', 'vm.dirty_background_bytes',
                    'kernel.sched_migration_cost_ns', 'kernel.sched_autogroup_enabled',
                    'vm.dirty_expire_centisecs', 'vm.dirty_writeback_centisecs', 'vm.nr_hugepages']
    kernel_knobs_kv = {}
    for knob in kernel_knobs:
        val = sp.check_output(['sysctl', '-n', knob])
        val = val.strip().decode('UTF-8')
        if knob == 'vm.nr_hugepages':
            curr = int((int(val) - 1) / nr_hugepages_100per * 100)
            if curr > 150:
                curr = 150
            elif curr < 50:
                curr = 50
            val = str(curr)
        kernel_knobs_kv[knob] = val

    with open(outputDir + "/knobs.json", "r") as f:
        curr_knobs = json.load(f, encoding = "UTF-8", object_pairs_hook=OrderedDict)
        curr_knobs['global']['global'].update(kernel_knobs_kv)
        
    with open(outputDir + "/knobs.json", "w") as f:
        f.write(json.dumps(curr_knobs, indent=4))


if __name__ == "__main__":
    main()
