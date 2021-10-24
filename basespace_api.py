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

    def download_rest_request(self, url, path):
        """Create a download folder and download file
        """
        dirname = self.project_id + os.sep + os.path.dirname(path)
        # print(dirname)
        if dirname != '':
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
        outfile = self.project_id + os.sep + path
        print("URL {} outfile {}".format(url, outfile))
        self.session.download_file(url, outfile)

    def download_projects(self):
        """Download project files
        """
        hreflist = []
        hrefcontentlist = []
        pathlist = []
        samplelist = []

        # Step 1: Find the Biosample ID from project id first
        # assume fewer than 1000 samples in a project
        resp_json = self.session.get_json(self.baseurl + 'biosamples?projectid=%s&access_token=%s&limit=1000' % (
            self.project_id, self.access_token))
        nSamples = len(resp_json['Items'])

        for sampleindex in range(nSamples):
            sampleid = resp_json['Items'][sampleindex]['Id']
            samplelist.append(sampleid)

        samplecsv = ','.join([str(i) for i in samplelist])
        print("Samples {}".format(samplecsv))

        # Step 2: Call API to get datasets based on biosample
        url = self.baseurl + \
            'datasets?inputbiosamples=%s&access_token=%s' % (
                samplecsv, self.access_token)

        json_obj = self.session.get_json(url)
        totalCount = int(json_obj['Paging']['TotalCount'])
        noffsets = int(math.ceil(float(totalCount)/1000.0))

        for index in range(noffsets):
            offset = 1000*index
            url = self.baseurl + 'datasets?inputbiosamples=%s&access_token=%s&limit=1000&Offset=%s' % (
                samplecsv, self.access_token, offset)
            json_obj = self.session.get_json(url)
            nDatasets = len(json_obj['Items'])
            for fileindex in range(nDatasets):
                href = json_obj['Items'][fileindex]['HrefFiles']
                hreflist.append(href)

        # Step 3: Get the download filepath (HrefContent) and filename (Path)
        # normally two files per dataset in our case
        for index in range(len(hreflist)):
            url = '%s?access_token=%s' % (hreflist[index], self.access_token)
            print("Step3 URL: {}".format(url))
            json_obj = self.session.get_json(url)
            nfiles = len(json_obj['Items'])
            for fileindex in range(nfiles):
                hrefcontent = json_obj['Items'][fileindex]['HrefContent']
                hrefcontentlist.append(hrefcontent)
                path = json_obj['Items'][fileindex]['Path']
                pathlist.append(path)

        for index in range(len(hreflist)):
            url = '%s?access_token=%s' % (
                hrefcontentlist[index], self.access_token)
            print(url)
            print('downloading %s' % (pathlist[index]))
            self.download_rest_request(url, pathlist[index])
