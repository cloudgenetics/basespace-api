import os
import boto3
import math
import requests
from http_session import HTTPSession


class BaseSpaceAPI():
    """BaseSpace Python API
    """

    def __init__(self, project_id,  access_token, url='https://api.euc1.sh.basespace.illumina.com/v2/') -> None:
        self.project_id = project_id
        self.access_token = access_token
        self.baseurl = url
        self.session = HTTPSession()

        # Get environment variables
        AWS_KEY = os.getenv('AWS_KEY')
        AWS_SECRET = os.environ.get('AWS_SECRET')
        self.AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_KEY,
            aws_secret_access_key=AWS_SECRET
        )

    def project_biosample_ids(self, maxsamples=1000):
        """Fetch BioSample IDs from a Project

        Args:
            limit (int): Maximum number of biosamples
        """
        # Find the Biosample ID from project id first  assume fewer than 1000 default max samples in a project
        response = self.session.get_json(self.baseurl + 'biosamples?projectid=%s&access_token=%s&limit=%d' % (
            self.project_id, self.access_token, maxsamples))

        biosamples = []
        for sample in response['Items']:
            biosamples.append(sample['Id'])

        return biosamples

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
        self.session.download_file(url, outfile)

    def upload_basespace_project_to_s3(self):
        """Download project files
        """
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
        
        # Download all datasets
        for dataset in datasets:
            url = '%s?access_token=%s' % (dataset['href'], self.access_token)
            print('Downloading %s' % (dataset['filename']))
            self.download_dataset(url, dataset['filename'])
            print('Fetching presigned URL')
            s3object = self.project_id + "/" + dataset['filename']
            response = self.s3_client.generate_presigned_post(
                Bucket=self.AWS_S3_BUCKET,
                Key=s3object,
                ExpiresIn=10
            )
            # Upload file to s3 using presigned URL
            files = {'file': open(s3object, 'rb')}
            r = requests.post(
                response['url'], data=response['fields'], files=files)
            print('Upload complete: {} status: {}'.format(
                s3object, r.status_code))
            # Remove file after upload
            if (r.status_code in [200, 201, 204]):
                os.remove(s3object)
            else:
                print("Error on uploading file {}".format(s3object))

        # Remove folder
        os.rmdir(self.project_id)
