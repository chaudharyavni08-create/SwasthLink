from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=150)
    password: str = Field(min_length=8, max_length=72)
    phone: str | None = Field(default=None, max_length=20)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=150)
    password: str = Field(min_length=8, max_length=72)


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    phone: str | None
    role_id: int
    is_active: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse