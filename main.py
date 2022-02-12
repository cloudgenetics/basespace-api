import sys
import optparse
import os

from basespace_api import BaseSpaceAPI
from multiprocessing.pool import ThreadPool
from functools import partial
import requests
from http_session import HTTPSession
import boto3
from botocore.exceptions import ClientError

def arg_parser():
    """Argument parser
    """
    parser = optparse.OptionParser()
    parser.add_option('-p', dest='projectid', help='Project ID: required')
    parser.add_option('-a', dest='accesstoken', help='Access Token: required')
    parser.add_option('-s', dest='s3bucket', help='s3bucket: required')
    (options, args) = parser.parse_args()

    try:
        if options.projectid == None:
            raise Exception
        if options.accesstoken == None:
            raise Exception
        if options.s3bucket == None:
            raise Exception
    except Exception:
        print("Usage: main.py -p <ProjectID> -a <AccessToken> -s <s3bucket>")
        sys.exit()

    return options

def project_mkdir(dir, fname):
    """Make directory for a project

    Args:
        dir (str): Path to create directory
        fname (str): Filename
    """
    
    dirname = dir + os.sep + os.path.dirname(fname)
    status = False
    if dirname != '':
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
            status = True
    return status

def download(dataset, projectid, access_token):
    url = '%s?access_token=%s' % (dataset['href'], access_token)
    fname = dataset['filename']
    print('Downloading %s' % (fname))
    # self.download_dataset(url, fname)
    project_mkdir(projectid, fname)
    outfile = projectid + os.sep + fname
    session = HTTPSession()
    session.download_file(url, outfile)

def upload(dataset, s3client, projectid, uuid, s3bucket):
    fname = dataset['filename']
    localfile = projectid + "/" + fname
    s3file = uuid + "/" + fname
    upload_status = 200

    try:
        response = s3client.upload_file(localfile, s3bucket, s3file)
    except ClientError as e:
        upload_status = 400

    file = {}
    file['url'] = 's3://' + s3bucket + '/' + s3file
    file['name'] = fname
    file['size'] = os.path.getsize(localfile)
    file['status'] = True if upload_status == 200 else False
    file['datasetid'] = uuid
    print('Upload complete')
    
if __name__ == "__main__":
    options = arg_parser()
    bs = BaseSpaceAPI(options.projectid, options.accesstoken, options.s3bucket, 'https://api.euc1.sh.basespace.illumina.com/v2/')
    datasets = bs.upload_basespace_project_to_s3('bs-eu-test')

    downpool = ThreadPool(processes=len(datasets)*2) 
    download_func = partial(download, projectid = options.projectid, access_token = options.accesstoken)
    downpool.map(download_func, datasets) 
    print("All downloads complete")
    s3 = boto3.client('s3') 
    uppool = ThreadPool(processes=len(datasets)*2)
    upload_func = partial(upload, s3, options.projectid, 'bs-eu-test', options.s3bucket)
    uppool.map(upload_func, datasets)

    '''
    for dataset in datasets:
        download(dataset, options.projectid, options.accesstoken)
    '''