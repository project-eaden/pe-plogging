import pytest
import logging

from pe_logging.logger_builder import (
    create_file_handler,
    create_stream_handler,
    LoggingConfig
)
from pe_logging import PELogger
from pe_logging.exceptions import LoggerConfigurationError


NAME = "test_logger"

@pytest.fixture
def tmp_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("tmp")
    return fn


# Test no file name with file handler specified fails
def test_unspecified_file_destination():
    with pytest.raises((LoggerConfigurationError, AssertionError)) as excinfo:
        _args = {
            "name":NAME, 
            "level":[logging.INFO], 
            "handler_types":['file'], 
        }
        PELogger(**_args)
        _args.update({"accepted_types": ['stream', 'file']}).pop("name")

        LoggingConfig(**_args)


# Test more levels than handlers fails
def test_handler_level_mismatch():
    with pytest.raises((LoggerConfigurationError, AssertionError)) as excinfo:
        _args = {
            "name":NAME, 
            "level":[logging.INFO, logging.DEBUG], 
            "handler_types":['stream'], 
        }
        PELogger(**_args)()
        _args.pop("name")
        LoggingConfig(**_args)

def test_multiple_handlers_single_level(tmp_dir):
    _args = {
        "name":NAME, 
        "level":[logging.INFO], 
        "handler_types":['file', 'stream'], 
        "file_path": tmp_dir / "test.log",
    }
    assert PELogger(**_args)()

def test_file_handler(tmp_dir):
    _args = {
        "name":NAME, 
        "level":[logging.WARNING, logging.INFO], 
        "handler_types":['file', 'stream'], 
        "file_path": tmp_dir / "test.log",
    }
    # Test base directory logging
    lg = PELogger(**_args)()
    lg.info("infotest")
    lg.warning("warningtest")

    # Check that only the relevant bits were written to the log
    with open(_args["file_path"], 'r') as f:
        body = " ".join(f.readlines())
        assert "warningtest" in body
        assert "infotest" not in body


# Test automatic directory creation behaviour for file handler
def test_log_dir_creation(tmp_dir):
    _args = {
        "name":NAME, 
        "level":[logging.WARNING, logging.INFO], 
        "handler_types":['file', 'stream'], 
        "file_path": tmp_dir / "logs" / "test.log",
    }
    lg = PELogger(**_args)()
    lg.warning("Easter egg moment :)")
    assert (tmp_dir / "logs").exists()
    assert (tmp_dir / "logs").is_dir()
    assert (tmp_dir / "logs" / "test.log").exists()