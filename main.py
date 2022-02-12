import sys
import optparse
from multiprocessing.pool import ThreadPool
from functools import partial
import shutil
import basespace_api as bs

def arg_parser():
    """Argument parser
    """
    parser = optparse.OptionParser()
    parser.add_option('-p', dest='projectid', help='Project ID: required')
    parser.add_option('-a', dest='accesstoken', help='Access Token: required')
    parser.add_option('-s', dest='s3bucket', help='s3bucket: required')
    parser.add_option('-u', dest='uuid', help='UUID: required')
    (options, args) = parser.parse_args()

    try:
        if options.projectid == None:
            raise Exception
        if options.accesstoken == None:
            raise Exception
        if options.s3bucket == None:
            raise Exception
    except Exception:
        print("Usage: main.py -p <ProjectID> -a <AccessToken> -s <s3bucket> -u <uuid>")
        sys.exit()

    return options

if __name__ == "__main__":
    options = arg_parser()
    # os.chdir('/mnt/efs/')
    datasets = bs.fetch_datasets(options.projectid, options.accesstoken, apiurl='https://api.euc1.sh.basespace.illumina.com/v2/')

    downpool = ThreadPool(processes=len(datasets)*2) 
    download_func = partial(bs.download, projectid = options.projectid, access_token = options.accesstoken)
    downpool.map(download_func, datasets) 
    print("All downloads complete")
    files = []
    for dataset in datasets:
        file = bs.upload(dataset, options.projectid, options.uuid, options.s3bucket)
        files.append(file)
    shutil.rmtree(options.projectid)