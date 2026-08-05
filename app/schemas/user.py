from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user_role import UserRole


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole

class UserRoleUpdate(BaseModel):
    role: UserRole
