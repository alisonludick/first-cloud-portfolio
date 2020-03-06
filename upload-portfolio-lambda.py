import json
import boto3
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:195783591734:deployPortfolioTopic')

    try:
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

        print("Job done")
        topic.publish(Subject="AWS Portfolio Deployed", Message="Potrfolio deployed successfully!")
    except:
        topic.publish(Subject="AWS Portfolio Deploy Failure", Message="Sorry, the Portfolio was not deployed successfully!")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
