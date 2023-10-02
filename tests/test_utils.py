from inspect import signature
from typing import List

import pytest


@pytest.fixture(scope="module")
def utils_imports(setup_imports):
    """Import required utility functions after patching imports."""
    from theTrial.utils.inspect_function import (
        get_first_arg_type,
        get_signature_details,
    )

    return get_first_arg_type, get_signature_details


@pytest.fixture
def sample_func_no_args():
    def _function():
        pass

    return _function


@pytest.fixture
def sample_func_with_args():
    def _function(x: int, y: List[str]):
        pass

    return _function


@pytest.fixture
def sample_func_without_annotations():
    def _function(x, y):
        pass

    return _function


@pytest.mark.parametrize(
    "func, expected",
    [
        ("sample_func_no_args", None),
        ("sample_func_with_args", int),
        ("sample_func_without_annotations", None),
    ],
)
def test_get_first_arg_type(utils_imports, request, func, expected):
    """Test the behavior of get_first_arg_type under various conditions."""
    get_first_arg_type, _ = utils_imports
    func_to_test = request.getfixturevalue(func)
    sig = signature(func_to_test)
    assert get_first_arg_type(sig) == expected


def test_test_get_first_arg_type_default_value(utils_imports, sample_func_no_args):
    """If default value is given, no args function should return the default."""
    get_first_arg_type, _ = utils_imports
    sig = signature(sample_func_no_args)
    default_value = str
    assert get_first_arg_type(sig, default=default_value) == str


@pytest.mark.parametrize(
    "func, num_args, expected_type",
    [
        ("sample_func_no_args", 0, None),
        ("sample_func_with_args", 2, int),
        ("sample_func_without_annotations", 2, None),
    ],
)
def test_get_signature_details(utils_imports, request, func, num_args, expected_type):
    """Test the behavior of get_signature_details under various conditions."""
    _, get_signature_details = utils_imports
    func_to_test = request.getfixturevalue(func)
    assert get_signature_details(func_to_test) == (num_args, expected_type)
