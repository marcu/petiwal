from datetime import datetime

from mastodon import Mastodon

import db
from entities import Petition
from settings import (
    MASTODON_ACCESS_TOKEN,
    MASTODON_API_BASE_URL,
    MASTODON_CLIENT_ID,
    MASTODON_CLIENT_SECRET,
)


def post_on_mapston(petition: Petition) -> None:
    """Create a post on Mastodon with the petition information"""

    # Initialize Mastodon client
    mastodon_client = Mastodon(
        client_id=MASTODON_CLIENT_ID,
        client_secret=MASTODON_CLIENT_SECRET,
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_API_BASE_URL,
    )

    # be sure to have all info for that petition
    petition.generate_missing_data()

    if len(petition.description_abstract) > 500:
        status_text = f"{petition.description_abstract_500} {petition.get_link()}"
        print("Using the 500 characters abstract.")
    else:
        # Text to post
        status_text = f"{petition.description_abstract} {petition.get_link()}"

    # Path to the image file
    image_path = f"./imgs/{petition.id}.png"

    # Upload the image
    media = mastodon_client.media_post(image_path, mime_type="image/png")

    # Post the status with the image
    mastodon_client.status_post(status_text, media_ids=[media["id"]])

    print("Posted successfully!")

    session = db.get_session()
    petition.mastodon_pub_date = datetime.now()
    session.commit()
