import json
import boto3

# {"BucketName": "image-upload-bucket-dev", "FileName": "value2"}


def get_signed_upload_url(event, context):

    # Parse event body to json
    event_body = json.loads(event["body"])

    # Create Boto3 client to connect with s3 services
    client = boto3.client("s3")

    expiration = event_body["Expiration"] if event_body.get(
        "Expiration") else 3600

    # Response object
    res = {
        "upload_url": None,
        "FileName": None,
        "ExpiresIn": expiration
    }

    # Generate Presigned url for Put operation
    try:
        res["upload_url"] = client.generate_presigned_url(ClientMethod="put_object",
                                                          Params={"Bucket": event_body.get("BucketName"),
                                                                  "Key": event_body.get("FileName")},
                                                          ExpiresIn=expiration,
                                                          HttpMethod="PUT"
                                                          )
    except Exception as e:
        print("[getSignedUrl] Error :: {}".format(e))

    response = {
        "statusCode": 200,
        "body": json.dumps({"url": res})
    }

    return response
