from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from fastapi import HTTPException, UploadFile
from src.core import config
import cloudinary
from cloudinary.api import delete_resources
from src.core import log

class CloudinaryService:
    def __init__(
        self,
    ):
        self.settings = cloudinary.config(
            cloud_name=config.cloudinary_config.CLOUDINARY_NAME,
            api_key=config.cloudinary_config.CLOUDINARY_API_KEY,
            api_secret=config.cloudinary_config.CLOUDINARY_API_SECRET,
            secure=True,
        )

    public_folder = f"user_posts/"

    @staticmethod
    def extract_public_id(image_url: str) -> str:
        try:
            result = image_url.split("/image/upload/")[-1]
            log.debug(f"Extracted public_id: {result}")
            return result
        except ValueError:
            raise ValueError("Invalid Cloudinary URL")


    async def upload(self, file: UploadFile, user_email: str):
        try:
            # Read the file content
            file_content = await file.read()

            # Wrap the file content in a BytesIO object
            from io import BytesIO
            file_like = BytesIO(file_content)

            # Upload the file to Cloudinary with a filename
            upload_result = upload(
                file=file_like,  # Pass the file-like object
                folder=f"{self.public_folder}{user_email}",
                overwrite=True,
                filename=file.filename  # Provide the original filename
            )

            # Retrieve `public_id` and `version`
            public_id = upload_result.get("public_id")
            version = upload_result.get("version")

            if not public_id:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve public_id from Cloudinary",
                )

            # Generate the correct URL
            result_url, _ = cloudinary_url(public_id, version=version)

            return result_url
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload to Cloudinary: {e}"
            )

    async def delete(self, public_id: str):
        try:
            # Удаляем конкретное изображение
            deleted_file_result = delete_resources(public_id)

            return {"deleted_file": deleted_file_result}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete image from Cloudinary: {e}"
            )


    async def resize(self, image_url: str, width: int, height: int, crop: str) -> str:
        try:
            url, _ = cloudinary_url(
                self.extract_public_id(image_url),
                width=width,
                height=height,
                crop=crop,
            )
            return url
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to resize image: {e}"
            )

    async def apply_filter(self, image_url: str, effect: str) -> str:
        print(f"Applying effect: {effect}")
        print(f"Image URL: {image_url}")
        public_id = self.extract_public_id(image_url)
        
        print(f"Extracted public_id: {public_id}")
        url, _ = cloudinary_url(
            public_id,
            transformation=[{"effect": effect}]
        )
        return url
    
    async def change_format_and_quality(self, image_url: str, quality: str, format: str) -> str:
        url, _ = cloudinary_url(
            self.extract_public_id(image_url), transformation=[{"quality": quality, "fetch_format": format}]
        )
        return url

cloudinary_service = CloudinaryService()