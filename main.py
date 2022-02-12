import sys
import optparse

from basespace_api import BaseSpaceAPI


def arg_parser():
    """Argument parser
    """
    parser = optparse.OptionParser()
    parser.add_option('-p', dest='projectid', help='Project ID: required')
    parser.add_option('-a', dest='accesstoken', help='Access Token: required')
    parser.add_option('-s', dest='s3bucket', help='S3bucet: required')
    parser.add_option('-u', dest='uuid', help='UUID: required')
    (options, args) = parser.parse_args()

    try:
        if options.projectid == None:
            raise Exception
        if options.accesstoken == None:
            raise Exception
        if options.s3bucket == None:
            raise Exception
        if options.uuid == None:
            raise Exception
    except Exception:
        print("Usage: main.py -p <ProjectID> -a <AccessToken> -s <s3bucket> -u <uuid>")
        sys.exit()

    return options


if __name__ == "__main__":
    options = arg_parser()
    bs = BaseSpaceAPI(options.projectid, options.accesstoken, options.s3bucket, url='https://api.euc1.sh.basespace.illumina.com/v2/')
    bs.upload_basespace_project_to_s3(options.uuid)
