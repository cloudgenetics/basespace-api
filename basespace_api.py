import os
import math
from http_session import HTTPSession


class BaseSpaceAPI():
    """BaseSpace Python API
    """

    def __init__(self, project_id,  access_token, url='https://api.basespace.illumina.com/v2/') -> None:
        self.project_id = project_id
        self.access_token = access_token
        self.baseurl = url
        self.session = HTTPSession()

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

    def download_dataset(self, url, path):
        """Download sample dataset

        Args:
            url (str): URL from which to download dataset
            path (str): Download path
        """
        self.project_mkdir(path)
        outfile = self.project_id + os.sep + path
        self.session.download_file(url, outfile)

    def download_projects(self):
        """Download project files
        """

        # Find the Biosample ID from project id first  assume fewer than 1000 samples in a project
        biosamples = self.project_biosample_ids(maxsamples=1000)

        samples_csv = ','.join([str(i) for i in biosamples])
        print("Samples {}".format(samples_csv))

        # Call API to get datasets based on biosamples
        url = self.baseurl + \
            'datasets?inputbiosamples=%s&access_token=%s' % (
                samples_csv, self.access_token)

        response = self.session.get_json(url)
        total_count = int(response['Paging']['TotalCount'])
        noffsets = int(math.ceil(float(total_count)/1000.0))

        hrefs = []
        hrefcontents = []
        paths = []

        for index in range(noffsets):
            offset = 1000*index
            url = self.baseurl + 'datasets?inputbiosamples=%s&access_token=%s&limit=1000&Offset=%s' % (
                samples_csv, self.access_token, offset)
            response = self.session.get_json(url)
            nDatasets = len(response['Items'])
            for fileindex in range(nDatasets):
                href = response['Items'][fileindex]['HrefFiles']
                hrefs.append(href)

        # Get the download filepath (HrefContent) and filename (Path)
        files = []
        for href in hrefs:
            url = '%s?access_token=%s' % (href, self.access_token)
            response = self.session.get_json(url)
            for dataset in response['Items']:
                hrefcontent = dataset['HrefContent']
                path = dataset['Path']
                files.append((hrefcontent, path))

        print("Files: {} ".format(files))

        for file in files:
            url = '%s?access_token=%s' % (file[0], self.access_token)
            print('downloading %s' % (file[0]))
            self.download_dataset(url, file[1])

        """
        for index in range(len(hrefs)):
            url = '%s?access_token=%s' % (hrefs[index], self.access_token)
            response = self.session.get_json(url)
            nfiles = len(response['Items'])
            for fileindex in range(nfiles):
                hrefcontent = response['Items'][fileindex]['HrefContent']
                hrefcontents.append(hrefcontent)
                path = response['Items'][fileindex]['Path']
                paths.append(path)
                print("File: {} href {} path {}".format(
                    fileindex, hrefcontent, path))

        for index in range(len(hrefcontents)):
            url = '%s?access_token=%s' % (
                hrefcontents[index], self.access_token)
            print('downloading %s' % (paths[index]))
            self.download_dataset(url, paths[index])
        """
