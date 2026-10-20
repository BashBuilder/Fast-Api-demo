import pytest

from app.calculations import add


@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (5, 5, 10)])
def test_add(num1: int, num2: int, expected: int):
  assert add(num1, num2) == expected
