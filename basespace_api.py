import os
import boto3
from botocore.exceptions import ClientError
import math
from http_session import HTTPSession

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
    # download_dataset(url, fname)
    project_mkdir(projectid, fname)
    outfile = projectid + os.sep + fname
    session = HTTPSession()
    session.download_file(url, outfile)
    print('Download complete %s' % (fname))

def upload(dataset, projectid, uuid, s3bucket):

    s3 = boto3.client('s3', region_name='us-east-2') 
    fname = dataset['filename']
    print("Uploading %s" %(fname))
    localfile = projectid + "/" + fname
    s3file = uuid + "/" + fname
    upload_status = 200
    try:
        response = s3.upload_file(localfile, s3bucket, s3file)
    except ClientError as e:
        upload_status = 400

    file = {}
    file['url'] = 's3://' + s3bucket + '/' + s3file
    file['name'] = fname
    file['size'] = os.path.getsize(localfile)
    file['status'] = True if upload_status == 200 else False
    file['datasetid'] = uuid
    return file

def fetch_datasets(project_id,  access_token, apiurl):
    """Fetch datasets
    """
    session = HTTPSession()
    # Call API to get datasets based on biosamples
    url = apiurl + \
        'datasets?projectid=%s&access_token=%s' % (
            project_id, access_token)

    response = session.get_json(url)
    total_count = int(response['Paging']['TotalCount'])
    noffsets = int(math.ceil(float(total_count)/1000.0))

    hrefs = []
    for index in range(noffsets):
        offset = 1000*index
        url = apiurl + 'datasets?projectid=%s&access_token=%s&limit=1000&Offset=%s' % (
            project_id, access_token, offset)
        response = session.get_json(url)
        nDatasets = len(response['Items'])
        for fileindex in range(nDatasets):
            href = response['Items'][fileindex]['HrefFiles']
            hrefs.append(href)
    
    # Get the download filepath (HrefContent) and filename (Path)
    datasets = []
    for href in hrefs:
        url = '%s?access_token=%s' % (href, access_token)
        response = session.get_json(url)
        for data in response['Items']:
            dataset = dict.fromkeys(['href', 'path'])
            dataset['href'] = data['HrefContent']
            dataset['filename'] = data['Path']
            datasets.append(dataset)

    return datasets
   
