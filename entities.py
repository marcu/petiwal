import json
import os
import re

from sqlalchemy import (
    # JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, relationship

from ia_tasks import (
    mistral_call,
    stability_generate_image,
)


class Base(DeclarativeBase):
    """Base class for all entities."""


class VoteHistory(Base):
    """Vote history entity"""

    __tablename__ = "vote_history"

    id = Column(Integer, primary_key=True)
    petition_id = Column(Integer, nullable=False)
    nbr_votes = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    petition_id = Column(Integer, ForeignKey("petitions.id"))
    petition = relationship("Petition", back_populates="vote_history")

    def __repr__(self):
        return f"<VoteHistory(id={self.id}, petition_id={self.petition_id}, vote={self.vote})>"


class Petition(Base):
    """Petition entity"""

    __tablename__ = "petitions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=False)
    description_abstract = Column(String, nullable=True, default=None)

    email = Column(String, nullable=True, default=None)

    # TODO fix it
    # keywords = Column(JSON)
    # keywords_en = Column(JSON)

    open_date = Column(Date, nullable=False)
    close_date = Column(Date, nullable=True, default=None)

    closed = Column(Boolean, nullable=False, default=False)

    instagram_pub_date = Column(DateTime, nullable=True, default=None)
    mastodon_pub_date = Column(DateTime, nullable=True, default=None)

    vote_history = relationship("VoteHistory", back_populates="petition")

    def __repr__(self):
        return f"<Petition(id={self.id}, title='{self.title}')>"

    def upsert(self, session):
        """Insert or update the petition in the database"""
        # get if exists
        petition = session.query(Petition).filter(Petition.id == self.id).first()
        # if exists, update
        if petition:
            petition.title = self.title
            petition.description = self.description
            petition.email = self.email
            petition.open_date = self.open_date
            petition.close_date = self.close_date
            petition.closed = self.closed
        else:
            petition = self

        session.add(petition)
        session.commit()

    def get_link(self):
        """Get the link to the petition"""
        return (
            f"https://www.parlement-wallonie.be/pwpages?p=petition-detail&id={self.id}"
        )

    def generate_petition_image(self):
        """Generate the image of the petition"""
        prompt_resume = f"Décrire en 2 phrases le contenu d'une image \
illustrant {self.description}"
        response_resume = mistral_call(prompt_resume)

        prompt_image_fr = f"Illustration, sans texte, graphique type \
bande dessinée affichant {response_resume}. Crayonné prononcé. Wallonie \
Belgique."
        response_resume_en = mistral_call(f"Translate in English the \
following text: {prompt_image_fr}")
        prompt_image_en = response_resume_en

        stability_generate_image(prompt_image_en, f"./imgs/{self.id}.png")

    def generate_keywords(self) -> dict:
        """Generate keywords for a petition"""
        prompt_fr = f"Peux tu me retourner le tableau JSON de 3 éléments \
contenant les trois mots clés \
qui décrivent le mieux la pétition dont le titre est {self.title} \
et le contenu est {self.description}"
        response_fr = mistral_call(prompt_fr)
        match_fr = re.search(r"\[(.*?)\]", response_fr, re.DOTALL)

        json_array_fr = None
        if match_fr:
            json_array_str_fr = f"[{match_fr.group(1)}]"
            # Parse the extracted JSON array
            json_array_fr = json.loads(json_array_str_fr)
        else:
            print("No JSON array found.")

        prompt_en = f"""Return the json which is the translation in english of
the following JSON :
```json
{json_array_str_fr}
```
"""
        response_en = mistral_call(prompt_en)
        match_en = re.search(r"\[(.*?)\]", response_en, re.DOTALL)

        json_array_en = None
        if match_en:
            json_array_str_en = f"[{match_en.group(1)}]"
            # Parse the extracted JSON array
            json_array_en = json.loads(json_array_str_en)
        else:
            print("No JSON array found.")

        return {"fr": json_array_fr, "en": json_array_en}

    def generate_petition_abstract(self) -> str:
        """Generate the abstract of a petition"""
        prompt_fr = f"Ecrire en 3 lignes le résumé de la pétition dont le \
    titre est {self.title} et le contenu est {self.description}"
        response_fr = mistral_call(prompt_fr)

        return response_fr

    def generate_missing_data(self) -> None:
        """Generate missing data for the petition"""
        # Generate the abstract
        if not self.description_abstract:
            self.description_abstract = self.generate_petition_abstract()

        # Generate the keywords
        # if not self.keywords or not self.keywords_en:
        #     keywords = self.generate_keywords()
        #     self.keywords = keywords["fr"]
        #     self.keywords_en = keywords["en"]

        # check if file exists imgs/{self.id}.png
        if not os.path.exists(f"imgs/{self.id}.png"):
            # Generate the image
            self.generate_petition_image()
