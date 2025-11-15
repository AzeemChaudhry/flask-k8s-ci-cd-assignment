# Unit tests for src/utils.py using pytest.
# Run locally with: pytest -q
# Simple unit test for the add function in utils.py
from src.utils import add


def test_add():
    """
    Test the add() function from utils.py.
    Ensures the function correctly adds two numbers.
    """
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
