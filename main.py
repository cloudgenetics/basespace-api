import sys
import optparse

from basespace_api import BaseSpaceAPI


def arg_parser():
    """Argument parser
    """
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
        print("Usage: main.py -p <ProjectID> -a <AccessToken>")
        sys.exit()

    return options


if __name__ == "__main__":
    options = arg_parser()
    bs = BaseSpaceAPI(options.projectid, options.accesstoken)
    bs.upload_basespace_project_to_s3()
