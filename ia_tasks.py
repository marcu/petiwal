import requests
from mistralai import Mistral

from settings import (
    MISTRAL_API_KEY,
    MISTRAL_MODEL,
    STABILITY_API_KEY,
    STABILITY_API_URL,
)


def mistral_call(prompt: str) -> str:
    """Make a call to mistral API using prompt"""
    mistral_client = Mistral(api_key=MISTRAL_API_KEY)

    chat_response = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return chat_response.choices[0].message.content


def stability_generate_image(prompt: str, output_image_path: str) -> None:
    """Generate an image using stability API"""
    response = requests.post(
        STABILITY_API_URL,
        headers={"authorization": f"Bearer {STABILITY_API_KEY}", "accept": "image/*"},
        files={"none": ""},
        data={
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": "1:1",
            # "model": STABILITY_MODEL,
        },
    )

    if response.status_code == 200:
        with open(output_image_path, "wb") as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
