import json
import boto3

# {"BucketName": "image-upload-bucket-dev", "FileName": "value2"}


def get_signed_upload_url(event, context):

    client = boto3.client("s3")
    expiration = event["Expiration"] if event.get("Expiration") else 3600
    try:
        url = client.generate_presigned_url('put_object',
                                            Params={"Bucket": event.get("BucketName"),
                                                    "Key": event.get("FileName")},
                                            ExpiresIn=expiration
                                            )
    except Exception as e:
        print("[getSignedUrl] Error :: {}".format(e))

    response = {
        "statusCode": 200,
        "body": json.dumps(url)
    }

    return response
