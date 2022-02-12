import os
import boto3
from botocore.exceptions import ClientError
import math
import requests
from http_session import HTTPSession
import shutil
import concurrent.futures
from multiprocessing import Pool, cpu_count
from functools import partial

class BaseSpaceAPI():
    """BaseSpace Python API
    """

    def __init__(self, project_id,  access_token, s3bucket, url) -> None:
        self.project_id = project_id
        self.access_token = access_token
        self.baseurl = url
        self.session = HTTPSession()
        self.uuid = None
        self.s3_client = boto3.client('s3')
        # Get environment variables
        self.AWS_S3_BUCKET = s3bucket
        
    def project_mkdir(self, path):
        """Make directory for a project

        Args:
            path (str): Path to create directory
        """
        
        dirname = self.project_id + os.sep + os.path.dirname(path)
        status = False
        if dirname != '':
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
                status = True
        return status

    def download_dataset(self, url, filename):
        """Download sample dataset

        Args:
            url (str): URL from which to download dataset
            path (str): Download path
        """
        
        self.project_mkdir(filename)
        outfile = self.project_id + os.sep + filename
        #self.session.download_file(url, outfile)

    def download_upload(self,dataset, uuid):
        url = '%s?access_token=%s' % (dataset['href'], self.access_token)
        fname = dataset['filename']
        print('Downloading %s' % (fname))
        # self.download_dataset(url, fname)
        self.project_mkdir(fname)
        outfile = self.project_id + os.sep + fname
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(outfile, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)

        localfile = self.project_id + "/" + fname
        s3file = uuid + "/" + fname
        upload_status = 200
        '''
        try:
            response = self.s3_client.upload_file(localfile, self.AWS_S3_BUCKET, s3file)
        except ClientError as e:
            upload_status = 400

        file = {}
        file['url'] = 's3://' + self.AWS_S3_BUCKET + '/' + s3file
        file['name'] = fname
        file['size'] = os.path.getsize(localfile)
        file['status'] = True if upload_status == 200 else False
        file['datasetid'] = uuid
        #files.append(file)
        print('Upload complete')
        '''
        
    def upload_basespace_project_to_s3(self, uuid):
        """Download project files
        """
        # os.chdir('/mnt/efs/')
        self.uuid = uuid
        # Call API to get datasets based on biosamples
        url = self.baseurl + \
            'datasets?projectid=%s&access_token=%s' % (
                self.project_id, self.access_token)

        response = self.session.get_json(url)
        total_count = int(response['Paging']['TotalCount'])
        noffsets = int(math.ceil(float(total_count)/1000.0))

        hrefs = []
        for index in range(noffsets):
            offset = 1000*index
            url = self.baseurl + 'datasets?projectid=%s&access_token=%s&limit=1000&Offset=%s' % (
                self.project_id, self.access_token, offset)
            response = self.session.get_json(url)
            nDatasets = len(response['Items'])
            for fileindex in range(nDatasets):
                href = response['Items'][fileindex]['HrefFiles']
                hrefs.append(href)
        
        # Get the download filepath (HrefContent) and filename (Path)
        datasets = []
        for href in hrefs:
            url = '%s?access_token=%s' % (href, self.access_token)
            response = self.session.get_json(url)
            for data in response['Items']:
                dataset = dict.fromkeys(['href', 'path'])
                dataset['href'] = data['HrefContent']
                dataset['filename'] = data['Path']
                datasets.append(dataset)

        '''       
        s3_client = boto3.client('s3')
        files = []
        # Download all datasets
        #for dataset in datasets:
        #with concurrent.futures.ThreadPoolExecutor() as exector : 
        #    exector.map(self.download_upload, datasets)
        pool = Pool(cpu_count())
        download_func = partial(self.download_upload, uuid = uuid)
        results = pool.map(download_func, datasets)
        pool.close()
        pool.join()
        # Remove folder
        shutil.rmtree(self.project_id)
        ''' 

        return datasets