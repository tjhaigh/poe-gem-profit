import argparse
from ninja import Ninja


def main(args):
    n = Ninja('Scourge')
    gems = n.get_skill_gems()
    gems = filter_gems(gems, args.include_awakened, args.include_alt_quality, 
                      args.include_double_corrupted, args.min_listings)
    calc_profit(gems)
    print_top_10(gems)

def filter_gems(gems, include_awakened, include_alt_quality, include_double_corrupted, min_listings):
    """ Filters the gem list based on whether awakened and alt quality are included
    """

    new_gems = []
    for gem in gems:
        # Reject any gems that have filtered mods
        if include_awakened == False and gem.is_awakened:
            continue
        if include_double_corrupted == False and gem.is_double_corrupted:
            continue
        if include_alt_quality == False and gem.is_alt_quality:
            continue
        if gem.count < min_listings:
            continue

        new_gems.append(gem)

    return new_gems


def calc_profit(gems):
    for gem in gems:
        base = [g for g in gems if gem.name == g.name and g.level == 1 and g.quality == 0 and g.corrupted == False]
        if len(base) == 1:
            base = base[0]
            gem.profit = gem.chaos_value - base.chaos_value


def print_top_10(gems):
    """ Sorts the given gem list by chaos value and prints the top 10

    """
    gems.sort(reverse=True, key=lambda gem: gem.profit)
    print("Top 10 gems by Profit:")
    print("-----------------------------")
    for x in range(10):
        gem = gems[x]
        print(gem.name, gem.chaos_value, gem.profit, gem.level, gem.quality, gem.corrupted)

    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Calculate optimal gems to level at a given time")
    parser.add_argument('--include-awakened', default=False, action='store_true',
        help='include awakened gems in the calcs')
    parser.add_argument('--include-alt-quality', default=False, action='store_true',
        help='include alt qualities in the calcs')
    parser.add_argument('--include-double-corrupted', default=False, action='store_true',
        help='include double corrupted gems in the calcs')
    parser.add_argument('--min-listings', type=int, default=1, help='Minimum number of listings to consider a gem')

    args = parser.parse_args()
    main(args)