import json
import os
from basespace_api import BaseSpaceAPI

def lambda_handler(event, context):
    # Get access token and project id
    
    data = event
    access_token = data['accessToken']
    projectid = data['projectId']
    uuid = data['uuid']
    s3bucket = data['s3bucket']
    apiurl = 'https://api.euc1.sh.basespace.illumina.com/v2/'
    if 'region' in data:
        region = data['region']
        if region == 'US':
            apiurl = 'https://api.basespace.illumina.com/v2/'
        if region == 'UK':
            apiurl = 'https://euw2.sh.basespace.illumina.com/v2/'
            
    # Create a BaseSpace instance
    bs = BaseSpaceAPI(projectid, access_token, s3bucket, apiurl)
    # Upload to S3
    files = bs.upload_basespace_project_to_s3(uuid)
    
    return {
        'statusCode': 200,
        'files': json.dumps(files)
    }