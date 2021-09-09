"""
Module test_01_utils
====================
Tests for the utils module.

Uses the files generated by the test_00_save.
"""
# standard
from pathlib import Path
# dev library
from npfc import utils
# debug
import logging
logging.basicConfig(level=logging.ERROR)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TESTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def test_check_arg_bool():
    """Test the parsing of arguments that should be bool only."""
    # should pass
    assert utils.check_arg_bool(True)
    # should throw a TypeError
    error = False
    try:
        assert utils.check_arg_bool(0)
    except TypeError:
        error = True
    assert error is True


def test_check_arg_positive_number():
    """Test the parsing of arguments that should be positive integers only."""
    # should pass
    assert utils.check_arg_positive_number(1)
    # should throw a ValueError
    error = False
    try:
        assert utils.check_arg_positive_number(0)
    except ValueError:
        error = True
    assert error is True
    # should throw a TypeError
    error = False
    try:
        assert utils.check_arg_positive_number('a')
    except TypeError:
        error = True
    assert error is True


def test_check_arg_input_file():
    """Test the parsing of arguments that should be a input file."""
    # should pass
    utils.check_arg_input_file('tests/tmp/test_save.sdf.gz')
    utils.check_arg_input_file('tests/tmp/test_save.csv.gz')
    # should throw a ValueError
    error = False
    try:
        utils.check_arg_input_file('tests/tmp/test_file_does_not_exist.csv')
    except ValueError:
        error = True
    assert error is True


def test_arg_output_file():
    """Test the parsing of arguments that should be an output file."""
    # should pass
    utils.check_arg_output_file('tests/tmp/test_new_file.csv')
    utils.check_arg_output_file('tests/tmp/test_new_file.csv.gz')
    utils.check_arg_output_file('tests/tmp/test_new_file.sdf')
    utils.check_arg_output_file('tests/tmp/test_new_file.sdf.gz')
    # should throw a ValueError
    error = False
    try:
        utils.check_arg_output_file('tests/tmp/test_file.csv.other')
    except ValueError:
        error = True
    assert error is True


def test_arg_config_file():
    """Test the parsing of arguments that should be a config file."""
    json_config = 'tests/tmp/std_protocol.json'
    # write file, it will be also tested for standardization later
    with open(json_config, 'w') as JSON:
        JSON.write('''{
                    "tasks": ["sanitize", "filter_molecular_weight"],
                    "filter_molecular_weight": "100.0 <= molecular_weight <= 1000.0"\n}''')
    # should pass
    utils.check_arg_config_file(json_config)
    # should throw a ValueError
    error = False
    try:
        utils.check_arg_config_file('tests/tmp/test.csv')
    except ValueError:
        error = True
    assert error is True
