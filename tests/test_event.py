from datetime import datetime

import pytest
from app.database.models import Event
from app.main import app
from app.routers.event import update_event

DATA_UPDATE_OPTIONS = [
    {}, {"test": "test"}, {"start": "20.01.2020"},
    {"start": datetime(2020, 2, 2), "end": datetime(2020, 1, 1)},
    {"start": datetime(2030, 2, 2)}, {"end": datetime(1990, 1, 1)},
    {"start": "2020-02-02", "end": "2021-12-21"},
]


def test_eventedit(client):
    response = client.get("/event/edit")
    assert response.status_code == 200
    assert b"Edit Event" in response.content


@pytest.mark.parametrize("data", DATA_UPDATE_OPTIONS)
def test_invalid_update(data, event, session):
    assert update_event(1, data, session) == None


def test_successful_update(event, session):
    data = {
        "title": "successful",
        "start": datetime(2021, 1, 20),
        "end": datetime(2021, 1, 21),
    }
    assert type(update_event(1, data, session)) == Event
    assert "successful" in update_event(1, data, session).title


def test_update_db_close(event):
    data = {
        "title": "Problem connecting to db",
    }
    assert update_event(1, data, db=None) == None


def test_update_event_does_not_exist(event, session):
    data = {
        "content": "An update test for an event does not exist"
    }
    assert update_event(5, data, db=session) == None
