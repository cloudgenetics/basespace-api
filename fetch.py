import math
import sys
import os
import optparse
from http_session import HTTPSession

BASEURL = 'https://api.basespace.illumina.com/v2/'


def arg_parser():
    parser = optparse.OptionParser()
    parser.add_option('-p', dest='projectid', help='Project ID: required')
    parser.add_option('-a', dest='accesstoken', help='Access Token: required')
    (options, args) = parser.parse_args()

    try:
        if options.projectid == None:
            raise Exception
        if options.accesstoken == None:
            raise Exception
    except Exception:
        print("Usage: fetch.py -p <projectid> -a <AccessToken>")
        sys.exit()

    return options


options = arg_parser()

projectid = options.projectid
AccessToken = options.accesstoken

hreflist = []
hrefcontentlist = []
pathlist = []
samplelist = []


def download_rest_request(url, path):
    dirname = projectid + os.sep + os.path.dirname(path)
    # print(dirname)
    if dirname != '':
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
    outfile = projectid + os.sep + path
    print("URL {} outfile {}".format(url, outfile))
    session.download_file(url, outfile)


# Step 1: Find the Biosample ID from project id first
# assume fewer than 1000 samples in a project
session = HTTPSession()
resp_json = session.get_json(BASEURL + 'biosamples?projectid=%s&access_token=%s&limit=1000' % (
    projectid, AccessToken))
nSamples = len(resp_json['Items'])

for sampleindex in range(nSamples):
    sampleid = resp_json['Items'][sampleindex]['Id']
    samplelist.append(sampleid)

samplecsv = ','.join([str(i) for i in samplelist])
print("Samples {}".format(samplecsv))

# Step 2: Call API to get datasets based on biosample
url = BASEURL + \
    'datasets?inputbiosamples=%s&access_token=%s' % (samplecsv, AccessToken)

json_obj = session.get_json(url)
totalCount = int(json_obj['Paging']['TotalCount'])
noffsets = int(math.ceil(float(totalCount)/1000.0))

for index in range(noffsets):
    offset = 1000*index
    url = BASEURL + 'datasets?inputbiosamples=%s&access_token=%s&limit=1000&Offset=%s' % (
        samplecsv, AccessToken, offset)
    json_obj = session.get_json(url)
    nDatasets = len(json_obj['Items'])
    for fileindex in range(nDatasets):
        href = json_obj['Items'][fileindex]['HrefFiles']
        hreflist.append(href)

# Step 3: Get the download filepath (HrefContent) and filename (Path)
# normally two files per dataset in our case
for index in range(len(hreflist)):
    url = '%s?access_token=%s' % (hreflist[index], AccessToken)
    print("Step3 URL: {}".format(url))
    json_obj = session.get_json(url)
    nfiles = len(json_obj['Items'])
    for fileindex in range(nfiles):
        hrefcontent = json_obj['Items'][fileindex]['HrefContent']
        hrefcontentlist.append(hrefcontent)
        path = json_obj['Items'][fileindex]['Path']
        pathlist.append(path)

for index in range(len(hreflist)):
    url = '%s?access_token=%s' % (hrefcontentlist[index], AccessToken)
    print(url)
    print('downloading %s' % (pathlist[index]))
    download_rest_request(url, pathlist[index])
