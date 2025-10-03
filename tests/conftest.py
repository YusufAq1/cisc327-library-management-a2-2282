import pytest
from database import init_database

@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database to its original form before each test."""
    init_database()
    yield
    # no teardown needed unless you want to delete DB after each test
