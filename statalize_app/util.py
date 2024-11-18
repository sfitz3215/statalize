def calculate_avg(hits, AB):
    if AB == 0:
        return 0
    return ("{:10.3f}".format(hits/AB))

def calculate_obp(hits, BB, AB):
    if AB == 0:
        return 0
    return ("{:10.3f}".format((hits + BB) / (AB + BB)))

def calculate_slg(singles, doubles, triples, HR, AB):
    if AB == 0:
        return 0
    total_bases = singles + (2 * doubles) + (3 * triples) + (4 * HR)
    return ("{:10.3f}".format(total_bases / AB))

def calculate_ops(OBP, SLG):
    SLG = float(SLG)
    OBP = float(OBP)
    return ("{:10.3f}".format(SLG + OBP))


def fix_bad_american_baseball_decimals(IP):
    IP_frac = IP % 1
    IP_whole = IP - IP_frac
    if IP_frac > 0:
        IP_frac *= 10
        IP_frac /= 3

    new_IP = IP_whole + IP_frac
    return new_IP


def calculate_WHIP(walks, hits, IP):
    if IP == 0:
        return 0
    new_IP = fix_bad_american_baseball_decimals(IP)
    return (walks + hits)/new_IP


def calculate_ERA(ER, IP):
    if IP == 0:
        return 0
    new_IP = fix_bad_american_baseball_decimals(IP)
    return (ER*9)/new_IP

