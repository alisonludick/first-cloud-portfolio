import boto3
import zipfile
import mimetypes

s3 = boto3.resource('s3')

portfolio_bucket = s3.Bucket('portfolio.acloudguru')
build_bucket = s3.Bucket('portfoliobuild.acloudguru')

build_bucket.download_file('portfoliobuild.zip', '/tmp/portfoliobuild.zip')

with zipfile.ZipFile('/tmp/portfoliobuild.zip') as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
          ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
