from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from helpers.database import get_db
from helpers.crud import create_image, get_image
from helpers.schemas import ImageCreate, ImageResponse
import io

app = FastAPI(title="SmartPlate Parking Lot Image System")

@app.post("/images/", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Handles the upload of an image file.
    This function validates the uploaded file to ensure it is an image,
    reads its content, and stores it in the database.
    Args:
        file (UploadFile): The uploaded file object. Must be an image file.
    Raises:
        HTTPException: If the uploaded file is not an image.
    Returns:
        The result of the `create_image` function, which typically includes
        details about the stored image in the database.
    """

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    content = await file.read()
    db = next(get_db())
    image_data = ImageCreate(
        filename=file.filename,
        content_type=file.content_type,
        data=content
    )
    return create_image(db, image_data)

@app.get("/images/{image_id}", response_model=ImageResponse)
async def retrieve_image(image_id: int):
    """
    Retrieve an image by its ID and return it as a streaming response.
    Args:
        image_id (int): The unique identifier of the image to retrieve.
    Returns:
        StreamingResponse: A streaming response containing the image data,
        with the appropriate content type and a Content-Disposition header
        for inline display.
    Raises:
        HTTPException: If the image with the given ID is not found, a 404
        HTTP exception is raised with the message "Image not found".
    """

    db = next(get_db())
    image = get_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(
        io.BytesIO(image.data),
        media_type=image.content_type,
        headers={"Content-Disposition": f"inline; filename={image.filename}"}
    )