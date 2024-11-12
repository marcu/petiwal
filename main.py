import argparse
import random
import sys
import time
from datetime import datetime

from db import get_session
from entities import Petition, VoteHistory
from mastodon_tasks import post_on_mapston
from scraping import get_petition_info, get_petition_list

import db

ACTION_UPDATE_PETITIONS = "update_petitions"
ACTION_POST_ON_MASTODON = "post_on_mastodon"


def update_petitions():
    """Update the petition stored in the database"""
    # get the list of the petitions
    petitions = get_petition_list()
    session = get_session()

    for petition in petitions:
        id_petition = petition["id"]
        is_open_petition = petition["is_open"]
        # check if the petition is already in the database
        petition = session.query(Petition).filter(
            Petition.id == id_petition).first()

        update_the_petition = True

        if petition:
            if petition.closed and not is_open_petition:
                # the petition is already closed
                update_the_petition = False

        if update_the_petition:
            # wait between 0.1 and 1 second
            time.sleep(random.uniform(0.1, 1))

            print(f"Fetching petition info for petition #{id_petition}")
            petition_info = get_petition_info(id_petition)

            print(petition_info)

            vote_count = petition_info["vote_count"]

            # delete to pass to the Petition constructor
            del petition_info["vote_count"]
            petition = Petition(**petition_info)
            petition.upsert(session)

            today_date = datetime.now().date()

            query = session.query(VoteHistory).filter(
                VoteHistory.petition_id == id_petition,
                VoteHistory.date == today_date
            )

            if query.count() == 0:
                vote_history = VoteHistory(
                    petition_id=id_petition, nbr_votes=vote_count,
                    date=today_date
                )
                session.add(vote_history)
            # else do nothing

            session.commit()
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "action",
        help="The action to perform",
        choices=[ACTION_UPDATE_PETITIONS, ACTION_POST_ON_MASTODON],
    )

    parser.add_argument("--petition_id", help="The petition id", type=int)

    args = parser.parse_args()

    if args.petition_id is None and args.action == ACTION_POST_ON_MASTODON:
        parser.error("Pour l'option choisie, l'argument petition_id est \
obligatoire.")

    if args.action == ACTION_UPDATE_PETITIONS:
        update_petitions()

    elif args.action == ACTION_POST_ON_MASTODON:
        petition_id = args.petition_id
        print("Posting on Mastodon for petition #", petition_id)

        session = db.get_session()
        petition = session.query(Petition).filter(Petition.id == petition_id).first()

        print(petition.description_abstract)

        if petition:
            petition.generate_missing_data()
            session.commit()
            post_on_mapston(petition)
        else:
            print(f"Petition #{petition_id} not found in the database")

    else:
        print("Action not implemented yet")
        sys.exit(1)
