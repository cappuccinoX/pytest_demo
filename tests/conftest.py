import logging
import pytest

@pytest.fixture()
def tips():
    logging.info('start')
    yield
    logging.info('end')