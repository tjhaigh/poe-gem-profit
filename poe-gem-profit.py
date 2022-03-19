import argparse
from ninja import Ninja
from tabulate import tabulate
import copy


def main(args):
    n = Ninja('Archnemesis')
    gems = n.get_skill_gems()
    currency = n.get_currency()
    gems = filter_gems(gems, args.include_awakened, args.include_alt_quality, 
                      args.include_double_corrupted, args.min_listings)
    gems = calc_profit(gems, currency)
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


def calc_profit(gems, currency):
    new_gems = []

    for gem in gems:
        variations = [g for g in gems if gem.name == g.name]
        base = [g for g in variations if g.level == 1 and g.quality == 0 and g.corrupted == False]
        # vaal gems rarely have a level 1 so we just don't calc profit for them
        # TODO: handle vaal gems
        if base == []:
            continue
        base = base[0]

        if gem.corrupted:
            # assumes brick is worth 0
            # TODO: handle bricks
            gem.chaos_value = gem.chaos_value / 8
        gem.profit = gem.chaos_value - base.chaos_value
        
        if gem.name == "Enlighten Support" and gem.level == 4:
            print(gem.chaos_value, gem.profit)
            print(base.chaos_value, base.level, base.corrupted)
        gem.profit_per_exp = gem.profit / gem.required_exp

        # For exceptional gems, add a variation which has 20q
        if gem.is_exceptional:
            gcp = [c for c in currency if c.details == 'gemcutters-prism']
            gcp = gcp[0]
            gcp_cost = gcp.chaos_value * 20

            gem_20q = copy.deepcopy(gem)
            gem_20q.quality = 20
            gem_20q.profit = gem_20q.profit - gcp_cost
            gem_20q.profit_per_exp = gem_20q.profit / (gem_20q.required_exp / 2) # exp is halved with 20q
            new_gems.append(gem_20q)
        
        new_gems.append(gem)
    
    return new_gems


def print_top_10(gems):
    """ Sorts the given gem list by chaos value and prints the top 10

    """
    gems.sort(reverse=True, key=lambda gem: gem.profit_per_exp)
    print("Top 10 gems by Profit:")
    print("-----------------------------")
    
    results = [[gem.name, gem.level, gem.quality, gem.corrupted, round(gem.chaos_value), round(gem.profit), "{:.2e}".format(gem.profit_per_exp)] for gem in gems[:20]]
    headers = ['Gem Name', 'Level', 'Quality', 'Corrupted', 'Value (chaos)', 'Profit', 'Profit per exp']

    print(tabulate(results, headers=headers))

    


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