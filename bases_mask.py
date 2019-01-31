class BaseMaskConfigException(Exception):
    """Raise if base mask for demux_reads is malformed"""

    pass


def split_bases_mask(bases_mask):
    """Parse a picard style bases mask
    and return a list of tuples
    e.g. for paired-end dual-indexed runs
    [('T', 100), ('B', 8), ('B', 8), ('T', 100)]"""
    splitat = []
    for i, c in enumerate(bases_mask):
        if c.isalpha():
            splitat.append(i)

    # Check that mask is well-behaved
    if splitat[0] == 0:
        raise BaseMaskConfigException("Mask must start with number of cycles, not type")
    # Check that no characters appear next to each other
    diffs = []
    for i in range(len(splitat) - 1):
        diffs.append(splitat[i + 1] - splitat[i])
    if (0 in diffs) or (1 in diffs):
        raise BaseMaskConfigException("Type characters must be separated by a number (of cycles)")

    result = []
    num = ""
    for i in range(len(bases_mask)):
        if not i in splitat:
            num += bases_mask[i]
        elif int(num) == 0:
            pass
        else:
            result.append((bases_mask[i], int(num)))
            num = ""

    return result


def compare_bases_mask(planned_reads, bases_mask):
    """Match user input bases mask to planned_reads from flowcell
    and decide if compatible."""

    planned = split_bases_mask(planned_reads)
    mask = split_bases_mask(bases_mask)

    lengths1 = [i[1] for i in planned]
    lengths2 = [i[1] for i in mask]
    if not sum(lengths1) == sum(lengths2):
        raise BaseMaskConfigException("Your base mask has more or fewer cycles than planned")

    matched_mask = []
    for type, cycles in planned:
        read = []
        s = 0
        while s < cycles:
            i = mask.pop(0)
            read.append(i)
            s += i[1]
        if s > cycles:
            raise BaseMaskConfigException("Your base mask has too many bases for a window")
        matched_mask.append(read)

    return matched_mask
