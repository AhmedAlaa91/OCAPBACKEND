# coding: utf-8
"""Utility functions"""
from __future__ import annotations

import os
from datetime import datetime


def Average(lst):
    return sum(lst) / len(lst)


def getenv(name: str, default: str = None) -> str:
    """Return environment variable value or default is not defined or blank"""
    value = os.environ.get(name)
    return value if value else default


def convert_str_bool(v: str, default=False) -> bool:
    """
    Convert string to boolean
    Return True if value is "true", "yes", "y" or "1"
    Return False if value is "false", "no", "n" or "0"
    Case is insensitive
    Return "default" arg otherwise
    """
    if v and v.lower() in ["true", "yes", "y", "1"]:
        return True
    if v and v.lower() in ["false", "no", "n", "0"]:
        return False
    return default


def convert_str_int(v: str, default=-1) -> int:
    """Convert string to integer. Return default in case of parsing error"""
    if v:
        try:
            return int(v)
        except:
            pass
    return default


def convert_iso_datetime(data: str) -> datetime:
    """Convert ISO formatted datetime string into datetime object or return None in case of invalid input"""
    try:
        return datetime.fromisoformat(data)
    except:
        return None
