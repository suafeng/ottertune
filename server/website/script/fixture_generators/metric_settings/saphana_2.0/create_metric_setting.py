#
# OtterTune - create_metric_settings.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#
import json
import shutil

# metrics type
COUNTER = 1
INFO = 2
STATISTICS = 3
# val type
STRING = 1
INTEGER = 2
REAL = 3
BOOL = 4
ENUM = 5
TIMESTAMP = 6

def main():
    with open('metrics_after.json', 'r') as f:
        ori_metrics = json.load(f);
    metrics = ori_metrics['global']

    final_metrics = []

    for table_name, metrics in ori_metrics['local']['table'].items():
        if len(metrics) > 0:
            mets = list(metrics.items())[0][1]
            for metrics_name, value in mets.items():
                entry = {}
                entry['model'] = 'website.MetricCatalog'
                fields = {}
                fields['name'] = '{}.{}'.format(table_name, metrics_name)
                fields['scope'] = 'table'
                fields['summary'] = ""
                fields['dbms'] = 10

                if table_name == 'm_table_statistics':
                    if 'count' in metrics_name:
                        fields['vartype'] = INTEGER
                        fields['metric_type'] = COUNTER
                    elif 'time' in metrics_name:
                        fields['vartype'] = TIMESTAMP
                        fields['metric_type'] = INFO
                    else:
                        fields['vartype'] = STRING
                        fields['metric_type'] = INFO
                elif table_name == 'm_caches' or table_name == 'm_disk_usage':
                    if 'count' in metrics_name or 'size' in metrics_name:
                        fields['vartype'] = INTEGER
                        fields['metric_type'] = COUNTER
                    elif 'time' in metrics_name:
                        fields['vartype'] = TIMESTAMP
                        fields['metric_type'] = INFO
                    else:
                        fields['vartype'] = STRING
                        fields['metric_type'] = INFO
                elif table_name == 'm_garbage_collection_statistics':
                    if 'count' in metrics_name:
                        fields['vartype'] = INTEGER
                        fields['metric_type'] = COUNTER
                    elif 'size' in metrics_name:
                        fields['vartype'] = REAL
                        fields['metric_type'] = STATISTICS
                    else:
                        fields['vartype'] = STRING
                        fields['metric_type'] = INFO
                elif table_name == 'm_host_resource_utilization':
                    if metrics_name == 'host':
                        fields['vartype'] = STRING
                        fields['metric_type'] = INFO
                    elif 'timestamp' in metrics_name:
                        fields['vartype'] = TIMESTAMP
                        fields['metric_type'] = INFO
                    else:
                        fields['vartype'] = INTEGER
                        fields['metric_type'] = STATISTICS
                elif table_name == 'm_workload':
                    if metrics_name == 'host' or metrics_name == 'port':
                        fields['vartype'] = STRING
                        fields['metric_type'] = INFO
                    elif 'rate' in metrics_name:
                        fields['vartype'] = REAL
                        fields['metric_type'] = STATISTICS
                    else:
                        fields['vartype'] = INTEGER
                        fields['metric_type'] = COUNTER



                entry['fields'] = fields
                final_metrics.append(entry)


    with open('saphana-2.0_metrics.json', 'w') as f:
        json.dump(final_metrics, f, indent=4)

if __name__ == '__main__':
    main()
