from datetime import datetime

from instagrapi import Client

import db
from entities import Petition
from settings import (
    INSTAGRAM_PASSWORD,
    INSTAGRAM_USERNAME,
)


def post_on_instagram(petition: Petition) -> None:
    """Create a post on Instagram with the petition information"""

    cl = Client()
    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

    # Upload a photo
    photo_path = f"./imgs/{petition.id}.png"
    caption = f"{petition.description_abstract} {petition.get_link()}"
    cl.photo_upload(photo_path, caption)

    print("Photo uploaded successfully!")

    session = db.get_session()
    petition.instagram_pub_date = datetime.now()
    session.commit()