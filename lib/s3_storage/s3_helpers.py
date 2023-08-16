import logging
import os

import boto3
from django.conf import settings

log = logging.getLogger(__name__)


def create_s3_client():
    os.environ["AWS_CA_BUNDLE"] = settings.AWS_CA_BUNDLE
    session = boto3.session.Session()
    client = session.client(
        verify=False,
        service_name="s3",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    log.info("create s3 client to upload file")
    return client, session


def create_aws_resource():
    s3 = boto3.resource(
        verify=False,
        service_name="s3",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    log.info("s3 Resource created")
    return s3


def generate_uploaded_file_url(key: str):
    client, session = create_s3_client()
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": key,
        },
        ExpiresIn=604800,
    )
    log.info(f"URL : {url}")
    return url


def get_cdr_file_by_key(key: str):
    try:
        s3, session = create_s3_client()
        incident_body = s3.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
        )
        log.info("File had been retrieved")
        return incident_body["Body"]
    except Exception as ex:
        log.error(f"Error {str(ex)}")
