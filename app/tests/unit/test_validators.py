import pytest

from pantry_chef.validators import is_not_empty_string


@pytest.mark.parametrize('value', ['', ' ', '  '])
def test_is_not_empty_string(value: str) -> None:
    assert is_not_empty_string(value) is False


@pytest.mark.parametrize('value', ['a', ' a', 'a ', ' a '])
def test_is_not_empty_string_true(value: str) -> None:
    assert is_not_empty_string(value) is True
