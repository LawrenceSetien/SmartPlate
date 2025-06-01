from sqlalchemy.orm import Session
from helpers.models import Image
from helpers.schemas import ImageCreate

def create_image(db: Session, image: ImageCreate):
    """
    Creates and stores an image record in the database.
    Args:
        db (Session): The database session used to interact with the database.
        image (ImageCreate): An object containing the image details, including
            filename, content type, and binary data.
    Returns:
        Image: The newly created image record from the database.
    """

    db_image = Image(
        filename=image.filename,
        content_type=image.content_type,
        data=image.data
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_image(db: Session, image_id: int):
    return db.query(Image).filter(Image.id == image_id).first()