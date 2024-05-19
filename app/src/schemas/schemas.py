import uuid
import enum
from typing import Dict, Hashable, List, Optional, Annotated, TypeVar
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr, PastDate, PlainSerializer, Strict, conset, UUID4
# from pydantic_extra_types.phone_numbers import PhoneNumber
from src.entity.models import Role, AssetType
from datetime import date


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=16)
    email: str
    phone: str = Field(min_length=10, max_length=13)
    birthday: date
    password: str = Field(min_length=4, max_length=10)


class UserUpdateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    phone: str = Field(min_length=10, max_length=13)
    birthday: date


class  RoleUpdateSchema(BaseModel):
    role: Role


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    phone: str | None
    birthday: date | None
    created_at: datetime
    avatar: str | None
    role: Role

    class Config:
        from_attributes = True


# class UserResponse(BaseModel):
#     user: UserDb
#     detail: str = "User successfully created"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str | None
    birthday: date | None
    created_at: datetime
    avatar: str | None
    role: Role
    model_config = ConfigDict(from_attributes=True)


class UserResponseAll(BaseModel):
    user: UserDb

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class CommentResponseSchema(BaseModel):
    id: int
    user_id: int
    photo_id: Annotated[UUID4, Strict(False)]
    text: str
    created_at: datetime
    updated_at: datetime


class CommentNewSchema(BaseModel):
    photo_id: Annotated[UUID4, Strict(False)]
    text: str


class PhotoBase(BaseModel):   
    url: str
    description: Optional[str] = Field(None, max_length=2200)    
    tags: Optional[conset(str, max_length=5)] # type: ignore
    asset_type: AssetType = AssetType.origin


class LinkType(enum.Enum):
    url: str = "URL"
    qr_code: str = "QR Code"

class TagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

# tags output format is controlled here

def tags_serializer(tags: TagBase) -> str:
    names = [f'#{tag.name}' for tag in tags]
    return " ".join(names)    


CustomStr = Annotated[List[TagBase], PlainSerializer(tags_serializer, return_type=str)]
UUIDString = Annotated[UUID4, PlainSerializer(lambda x: str(x), return_type=str)]


class SimpleComment(BaseModel):
    user_id: int
    text: str


class PhotoResponse(PhotoBase):
    id: Annotated[UUID4, Strict(False)]
    created_at: datetime
    updated_at: datetime
    url: str
    # tags: list[TagBase]
    tags: CustomStr
    comments: list[SimpleComment]

    class Config:
        from_attributes = True


class PhotoTransform(BaseModel):
    ...
