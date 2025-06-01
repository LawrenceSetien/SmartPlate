from pydantic import BaseModel

class ImageCreate(BaseModel):
    filename: str
    content_type: str
    data: bytes

class ImageResponse(BaseModel):
    id: int
    filename: str
    content_type: str

    class Config:
        orm_mode = True