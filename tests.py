__author__ = "AivanF"

import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app import app
from db import delete_database, create_database


test_cases_post = [
    dict(name="foo", data=dict(pw="pi"), res=404),
    dict(name="bar", data=dict(code="phi"), res=404),
    dict(name="jat", data=dict(code="eu", extra="smth"), res=200),
    dict(name="null", data=dict(code="eu", python="cool"), res=200),
    dict(name="jat", data=dict(code="pi"), res=200),
]
test_cases_get = [
    dict(name="foo", count=0),
    dict(name="bar", count=0),
    dict(name="jat", count=2),
    dict(name="null", count=1),
]


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
@pytest.mark.asyncio
async def get_db():
    await delete_database()
    await create_database()


@pytest.mark.parametrize("test_case", test_cases_post)
def test_post(get_db, test_case):
    with TestClient(app)() as client:
        response = client.post(f"/{test_case['name']}", json=test_case["data"])
        assert response.status_code == test_case["res"]


@pytest.mark.parametrize("test_case", test_cases_get)
def test_get(get_db, test_case):
    with TestClient(app)() as client:
        response = client.get(f"/{test_case['name']}")
        assert len(response.json()) == test_case["count"]
