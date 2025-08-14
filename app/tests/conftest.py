from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app as tapp


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(tapp) as client:
        yield client
