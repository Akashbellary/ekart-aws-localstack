from fastapi import UploadFile
from config.database import s3_client, ENV
import uuid

async def upload_product_image(product_id: str, file: UploadFile) -> str:
    """Upload product image to S3"""
    bucket_name = f"ekart-product-images-{ENV}"
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    file_key = f"products/{product_id}/{uuid.uuid4()}.{file_ext}"
    
    try:
        # Read file content
        content = await file.read()
        
        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=content,
            ContentType=file.content_type
        )
        
        # Return public URL (LocalStack format)
        return f"http://localhost:4566/{bucket_name}/{file_key}"
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise
