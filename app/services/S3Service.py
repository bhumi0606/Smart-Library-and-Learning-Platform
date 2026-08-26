import boto3

from app.core.config import settings


s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def upload_document(
    file_bytes: bytes,
    file_name: str,
    content_type: str,
):

    s3_client.put_object(
        Bucket=settings.AWS_S3_BUCKET,
        Key=file_name,
        Body=file_bytes,
        ContentType=content_type,
    )

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_S3_BUCKET,
            "Key": file_name,
        },
        ExpiresIn=3600,
    )