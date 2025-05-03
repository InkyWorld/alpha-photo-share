from enum import Enum
from fastapi import APIRouter, status, HTTPException, Depends, UploadFile
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.repository.transformed_images import get_all_for_user, get as get_ti, save as save_ti, get_by_url
from src.models.transformed_images import TransformedImage
from src.schemas.enums import CloudinaryCropEnum, CloudinaryEffectEnum, CloudinaryQualityEnum, CloudinaryFormatEnum
from src.services.qr_code import qrcode_service
from src.services.image import cloudinary_service
from src.db.database import get_db
from src.services.auth import auth_service
from src.models.users import User
from src.repository.posts import get_post
from src.core import log
from src.schemas.images import TransformResponseImageSchema

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/resize", response_model=TransformResponseImageSchema, status_code=status.HTTP_201_CREATED)
async def resize(
    post_id: UUID,
    width: int,
    height: int,
    crop: CloudinaryCropEnum,

    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        log.error(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="post not found")
    image_url = post.image_url
    transformed_url = await cloudinary_service.resize(image_url, width, height, crop.value)
    transformed_image_in_db = await get_by_url(transformed_url, db)
    if transformed_image_in_db:
        return transformed_image_in_db
    transformed_image = await save_ti(user.id, post_id, transformed_url, db)
    return transformed_image

@router.post("/apply_filter", response_model=TransformResponseImageSchema, status_code=status.HTTP_201_CREATED)
async def apply_filter(
    post_id: UUID,
    effect: CloudinaryEffectEnum,
    value: int,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        log.error(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="post not found")
    limits = {
        "blur": (1, 200),
        "pixelate": (1, 200),
        "oil_paint": (1, 100),
        "brightness": (-99, 100),
        "contrast": (-100, 100),
        "saturation": (-100, 100),
        "hue": (0, 360),
        "gamma": (0.01, 9.99),
        "sharpen": (1, 100),
        "vignette": (1, 100),
    }
    min_val, max_val = limits.get(effect.value, (None, None))

    if min_val is not None and not (min_val <= value <= max_val):
        raise HTTPException(
            status_code=400,
            detail=f"Effect '{effect.value}' must be in range [{min_val}, {max_val}].",
        )

    effect_string = f"{effect.value}:{value}"
    image_url = post.image_url
    transformed_url = await cloudinary_service.apply_filter(image_url, effect_string)
    transformed_image_in_db = await get_by_url(transformed_url, db)
    if transformed_image_in_db:
        return transformed_image_in_db
    transformed_image = await save_ti(user.id, post_id, transformed_url, db)
    return transformed_image

@router.post("/reduce_size", response_model=TransformResponseImageSchema, status_code=status.HTTP_201_CREATED)
async def reduce_size(
    post_id: UUID,
    quality: CloudinaryQualityEnum,
    format: CloudinaryFormatEnum,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        log.error(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="post not found")
    image_url = post.image_url
    transformed_url = await cloudinary_service.change_format_and_quality(image_url, quality.value, format.value)
    transformed_image_in_db = await get_by_url(transformed_url, db)
    if transformed_image_in_db:
        return transformed_image_in_db
    transformed_image = await save_ti(user.id, post_id, transformed_url, db)
    return transformed_image


@router.get("/user_transformed_images", response_model=list[TransformResponseImageSchema])
async def get_transformed_images_for_user(user: User = Depends(auth_service.authenticate_user), db: AsyncSession = Depends(get_db)):
    user_id = user.id
    images = await get_all_for_user(user_id, db)
    if not images:
        raise HTTPException(status_code=404, detail="No transformed images found")
    return images


@router.get("/transformed_image/{id}", response_model=TransformResponseImageSchema)
async def get_transformed_image(id: UUID, db: AsyncSession = Depends(get_db)):
    image = await get_ti(id, db)
    if not image:
        raise HTTPException(status_code=404, detail="Transform image not found")
    return image
