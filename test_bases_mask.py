import pytest

from bases_mask import *


def test_parse1():
    bases_mask1 = "100T8B8B100T"
    x = split_bases_mask(bases_mask1)
    assert [("T", 100), ("B", 8), ("B", 8), ("T", 100)] == x


def test_parse2():
    bases_mask1 = "100T8B7B1S100T"
    x = split_bases_mask(bases_mask1)
    assert [("T", 100), ("B", 8), ("B", 7), ("S", 1), ("T", 100)] == x


def test_parse3():
    bases_mask1 = "100T8B0B100T"
    x = split_bases_mask(bases_mask1)
    assert [("T", 100), ("B", 8), ("T", 100)] == x


def test_parse4():
    bases_mask1 = "100T8B00B100T"
    x = split_bases_mask(bases_mask1)
    assert [("T", 100), ("B", 8), ("T", 100)] == x


def test_parse5():
    bases_mask1 = "T8B00B100T"
    with pytest.raises(BaseMaskConfigException):
        x = split_bases_mask(bases_mask1)


def test_parse6():
    bases_mask1 = "100TT8B10B100T"
    with pytest.raises(BaseMaskConfigException):
        x = split_bases_mask(bases_mask1)


def test_compatibility0():
    """demux_reads and planned_reads are the same"""
    planned_reads = "100T8B8B100T"
    user_mask = "100T8B8B100T"
    assert compare_bases_mask(planned_reads, user_mask)


def test_compatibility1():
    """demux_reads is compatible with planned reads"""
    planned_reads = "100T8B8B100T"
    user_mask = "100T8B7B1S100T"
    assert compare_bases_mask(planned_reads, user_mask)


def test_compatibility2():
    planned_reads = "100T8B8B100T"
    user_mask = "90T10S8B8B100T"
    assert compare_bases_mask(planned_reads, user_mask)


def test_compatibility3():
    """Total lengths differ"""
    planned_reads = "100T8B8B100T"
    user_mask = "100T8B10B100T"
    with pytest.raises(BaseMaskConfigException):
        compare_bases_mask(planned_reads, user_mask)
