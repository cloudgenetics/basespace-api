import requests
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


def get_json(url):
    r = requests.get(url)
    return r.json()


def downloadrestrequest(url, path):
    dirname = projectid + os.sep + os.path.dirname(path)
    # print(dirname)
    if dirname != '':
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    outfile = projectid + os.sep + path
    r = requests.get(url)
    with open(outfile, 'wb') as f:
        f.write(r.content)


options = arg_parser()

projectid = options.projectid
AccessToken = options.accesstoken

hreflist = []
hrefcontentlist = []
pathlist = []
samplelist = []

# Step 1: Find the Biosample ID from project id first
# assume fewer than 1000 samples in a project
session = HTTPSession(baseurl=BASEURL)
json_obj = session.get_json('biosamples?projectid=%s&access_token=%s&limit=1000' % (
    projectid, AccessToken))
nSamples = len(json_obj['Items'])

for sampleindex in range(nSamples):
    sampleid = json_obj['Items'][sampleindex]['Id']
    samplelist.append(sampleid)

samplecsv = ','.join([str(i) for i in samplelist])
print(samplecsv)

# Step 2: Call API to get datasets based on biosample
url = 'datasets?inputbiosamples=%s&access_token=%s' % (samplecsv, AccessToken)

json_obj = session.get_json(url)
totalCount = int(json_obj['Paging']['TotalCount'])
noffsets = int(math.ceil(float(totalCount)/1000.0))

for index in range(noffsets):
    offset = 1000*index
    url = 'datasets?inputbiosamples=%s&access_token=%s&limit=1000&Offset=%s' % (
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
    json_obj = get_json(url)
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
    downloadrestrequest(url, pathlist[index])
