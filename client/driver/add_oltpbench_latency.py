import sys
import os
import glob
import json
from collections import OrderedDict

# take oltpbench home and controller output dir as argument


def main():
    if (len(sys.argv) != 3):
        raise Exception(
            "Usage: python add_oltpbench_latency.py [OLTP-Bench Directory] [Controller Output Directory]")

    # output file named as outputfile.*
    oltpOutputDir = sys.argv[1] + '/results'
    conOutputDir = sys.argv[2]

    summary_file = sorted(glob.glob(oltpOutputDir + '/outputfile*.summary'),
                          key=os.path.getmtime)[-1]

    # read oltpbench output summary
    with open(summary_file) as f:
        summary = json.load(f, encoding='UTF-8', object_pairs_hook=OrderedDict)
        latency_99th = summary['Latency Distribution']['99th Percentile Latency (microseconds)']
        
    # add latency
    with open(conOutputDir + "/metrics_before.json", "r") as f:
        conf_before = json.load(f,
                                encoding="UTF-8",
                                object_pairs_hook=OrderedDict)
        conf_before['global']['udf'] = OrderedDict([("latency", "0")])

    with open(conOutputDir + "/metrics_after.json", "r") as f:
        conf_after = json.load(f,
                               encoding="UTF-8",
                               object_pairs_hook=OrderedDict)
        conf_after['global']['udf'] = OrderedDict(
            [("latency", str(latency_99th))])

    with open(conOutputDir + "/metrics_before.json", "w") as f:
        f.write(json.dumps(conf_before, indent=4))

    with open(conOutputDir + "/metrics_after.json", "w") as f:
        f.write(json.dumps(conf_after, indent=4))


if __name__ == "__main__":
    main()
