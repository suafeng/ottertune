import argparse
import logging
import os
import requests
import glob

# this file upload all results stored in this directory

# Logging
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

# for example, if the summary file is /home/tdai1/results/1541124265__summary.json,
# datadir should be /home/tdai1/results/ and timestamp should be 1541124265
def upload_one_set(datadir, timestamp, upload_code, url):
    params = {
        'summary': open(os.path.join(datadir, timestamp + '__summary.json'), 'rb'),
        'knobs': open(os.path.join(datadir, timestamp + '__knobs.json'), 'rb'),
        'metrics_before': open(os.path.join(datadir, timestamp + '__metrics_before.json'), 'rb'),
        'metrics_after': open(os.path.join(datadir, timestamp + '__metrics_after.json'), 'rb'),
    }

    response = requests.post(url,
                             files=params,
                             data={'upload_code': upload_code})
    LOG.info(response.content)

def upload(datadir, upload_code, url):
    summary_json =  sorted(glob.glob(datadir + '*__summary.json'), key=os.path.getmtime)
    
    for i in range(len(summary_json)):
        curr_summary_json = summary_json[i]
        timestamp = curr_summary_json.split('/')[-1].split('__')[0]
        upload_one_set(datadir, timestamp, upload_code, url)


def main():
    parser = argparse.ArgumentParser(description="Upload generated data to the website")
    parser.add_argument('datadir', type=str, nargs=1,
                        help='Directory containing the generated data')
    parser.add_argument('upload_code', type=str, nargs=1,
                        help='The website\'s upload code')
    parser.add_argument('url', type=str, default='http://0.0.0.0:8000/new_result/',
                        nargs='?', help='The upload url: server_ip/new_result/')
    args = parser.parse_args()
    upload(args.datadir[0], args.upload_code[0], args.url)


if __name__ == "__main__":
    main()
