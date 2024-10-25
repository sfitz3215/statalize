def calculate_avg(hits, AB):
    if AB == 0:
        return 0
    return hits / AB

def calculate_obp(hits, BB, AB):
    if AB == 0:
        return 0
    return (hits + BB) / (AB + BB)

def calculate_slg(singles, doubles, triples, HR, AB):
    if AB == 0:
        return 0
    total_bases = singles + (2 * doubles) + (3 * triples) + (4 * HR)
    return total_bases / AB

def calculate_ops(OBP, SLG):
    return SLG + OBP