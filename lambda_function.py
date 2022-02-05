import json
import os
from basespace_api import BaseSpaceAPI

def lambda_handler(event, context):
    # Get access token and project id
    
    data = event
    access_token = data['accessToken']
    projectid = data['projectId']
    uuid = data['uuid']
    apiurl = 'https://api.euc1.sh.basespace.illumina.com/v2/'
    if 'apiurl' in data:
        apiurl = data['url']
        
    # Create a BaseSpace instance
    bs = BaseSpaceAPI(projectid, access_token, apiurl)
    # Upload to S3
    files = bs.upload_basespace_project_to_s3(uuid)
    
    return {
        'statusCode': 200,
        'files': json.dumps(files)
    }