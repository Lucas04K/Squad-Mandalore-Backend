# from tests.define_test_variables import client

from datetime import date
import pytest
from src.models.models import Athlete, Base, Gender, Trainer
from src.services.csv_service import create_csv, parse_csv


@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Replace the connection string with your actual database connection details.
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    #engine = create_engine("sqlite:///db/test_test.db", echo=True, connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

def create_athletes(session):
    trainer = Trainer(username="trainer_athlete", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer", uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()

    trainerDb = session.query(Trainer).filter(Athlete.username == "trainer_athlete").first()
    athlete = Athlete(username="athlete", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete", birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer_id=trainerDb.id)
    session.add(athlete)
    session.commit()

    athlete2 = Athlete(username="athlete2", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete", birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer_id=trainerDb.id)
    session.add(athlete2)
    session.commit()

def test_csv(session):
    create_athletes(session)
    create_csv(session)
    parse_csv()