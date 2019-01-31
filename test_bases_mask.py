import pytest


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


def test_compatibility1():
    planned_reads = "100T8B8B100T"
    user_mask = "100T8B7B1S100T"
    assert compare_bases_mask(planned_reads, user_mask)  # == True


def test_compatibility2():
    planned_reads = "100T8B8B100T"
    user_mask = "100T8B10B100T"
    assert compare_bases_mask(planned_reads, user_mask) == False
