import json
import os
from basespace_api import BaseSpaceAPI

def lambda_handler(event, context):
    # Get access token and project id
    data = event
    access_token = data['accessToken']
    projectid = data['projectId']
    uuid = data['uuid']
    # Create a BaseSpace instance
    bs = BaseSpaceAPI(projectid, access_token)
    # Upload to S3
    bs.upload_basespace_project_to_s3(uuid)
    return {
        'statusCode': 200,
        'body': 'success'
    }