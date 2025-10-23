"""
Module for generating detailed statistics about the draw
"""

from collections import Counter, defaultdict
from typing import Dict, List
from .champions_league_draw import ChampionsLeagueDraw, create_sample_teams, Team


class DrawStatistics:
    """Generate detailed statistics about a draw"""
    
    def __init__(self, draw: ChampionsLeagueDraw):
        self.draw = draw
        self.teams = draw.teams
    
    def country_matchups(self) -> Dict[str, Dict[str, int]]:
        """Count matches between countries"""
        matchups = defaultdict(lambda: defaultdict(int))
        
        for team in self.teams:
            for opponent, _ in self.draw.fixtures[team]:
                if team.country != opponent.country:
                    countries = tuple(sorted([team.country, opponent.country]))
                    matchups[countries[0]][countries[1]] += 1
        
        return dict(matchups)
    
    def pot_matchups(self) -> Dict[int, Dict[int, int]]:
        """Count matches between pots"""
        matchups = defaultdict(lambda: defaultdict(int))
        
        for team in self.teams:
            for opponent, _ in self.draw.fixtures[team]:
                pot1, pot2 = sorted([team.pot, opponent.pot])
                matchups[pot1][pot2] += 1
        
        return dict(matchups)
    
    def home_away_balance_check(self) -> Dict[str, int]:
        """Check home/away balance for each team"""
        balance = {}
        
        for team in self.teams:
            home = sum(1 for _, is_home in self.draw.fixtures[team] if is_home)
            away = sum(1 for _, is_home in self.draw.fixtures[team] if not is_home)
            balance[team.name] = {'home': home, 'away': away, 'difference': abs(home - away)}
        
        return balance
    
    def display_statistics(self):
        """Display all statistics"""
        
        print("\n" + "="*80)
        print("DRAW STATISTICS")
        print("="*80 + "\n")
        
        # General statistics
        print("GENERAL STATISTICS")
        print("-" * 80)
        print(f"Total teams: {len(self.teams)}")
        print(f"Total matches: {sum(len(fixtures) for fixtures in self.draw.fixtures.values()) // 2}")
        print(f"Matches per team: 8 (4 home, 4 away)")
        
        # Distribution by pot
        print("\nDISTRIBUTION BY POT")
        print("-" * 80)
        for pot in [1, 2, 3, 4]:
            teams_in_pot = [t for t in self.teams if t.pot == pot]
            countries = Counter(t.country for t in teams_in_pot)
            print(f"Pot {pot}: {len(teams_in_pot)} teams")
            print(f"  Countries: {dict(countries)}")
        
        # Matches between pots
        print("\nMATCHES BETWEEN POTS")
        print("-" * 80)
        pot_matchups = self.pot_matchups()
        for pot1 in sorted(pot_matchups.keys()):
            for pot2 in sorted(pot_matchups[pot1].keys()):
                count = pot_matchups[pot1][pot2]
                print(f"Pot {pot1} vs Pot {pot2}: {count} matches")
        
        # Statistics by country
        print("\nSTATISTICS BY COUNTRY")
        print("-" * 80)
        countries_stats = defaultdict(lambda: {'teams': 0, 'matches': 0, 'home': 0, 'away': 0})
        
        for team in self.teams:
            countries_stats[team.country]['teams'] += 1
            countries_stats[team.country]['matches'] += len(self.draw.fixtures[team])
            countries_stats[team.country]['home'] += sum(1 for _, is_home in self.draw.fixtures[team] if is_home)
            countries_stats[team.country]['away'] += sum(1 for _, is_home in self.draw.fixtures[team] if not is_home)
        
        for country in sorted(countries_stats.keys()):
            stats = countries_stats[country]
            print(f"{country}: {stats['teams']} team(s), {stats['matches']} matches "
                  f"({stats['home']} home, {stats['away']} away)")
        
        # Home/away balance
        print("\nHOME/AWAY BALANCE")
        print("-" * 80)
        balance = self.home_away_balance_check()
        max_diff = max(balance.values(), key=lambda x: x['difference'])['difference']
        print(f"Maximum difference: {max_diff} (should be 0)")
        
        if max_diff == 0:
            print("Perfect balance for all teams!")
        else:
            unbalanced = [(name, b) for name, b in balance.items() if b['difference'] > 0]
            for name, b in unbalanced:
                print(f"Warning: {name}: {b['home']} home, {b['away']} away")
        
        # Constraint verification
        print("\nCONSTRAINT VERIFICATION")
        print("-" * 80)
        
        all_valid = True
        
        for team in self.teams:
            if len(self.draw.fixtures[team]) != 8:
                print(f"ERROR: {team.name}: {len(self.draw.fixtures[team])} matches (should be 8)")
                all_valid = False
        
        for team in self.teams:
            for pot in [1, 2, 3, 4]:
                count = self.draw.opponents_by_pot[team][pot]
                if count != 2:
                    print(f"ERROR: {team.name}: {count} opponents from pot {pot} (should be 2)")
                    all_valid = False
        
        for team in self.teams:
            for opponent, _ in self.draw.fixtures[team]:
                if opponent.country == team.country:
                    print(f"ERROR: {team.name} plays {opponent.name} (same country)")
                    all_valid = False
        
        if all_valid:
            print("All constraints satisfied!")
            print("- 8 matches per team")
            print("- 4 home matches, 4 away matches")
            print("- 2 opponents from each pot")
            print("- No teams from same country play each other")


def main():
    """Main function"""
    
    print("\n" + "=" * 70)
    print("CHAMPIONS LEAGUE DRAW STATISTICS")
    print("=" * 70)
    
    print("\nGenerating draw...")
    teams = create_sample_teams()
    draw = ChampionsLeagueDraw(teams)
    
    if draw.perform_draw(max_attempts=15000):
        print("\nAnalyzing statistics...")
        stats = DrawStatistics(draw)
        stats.display_statistics()
    else:
        print("\nUnable to generate a valid draw")


if __name__ == "__main__":
    main()
