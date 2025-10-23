"""
Champions League Draw System
2024-2025 format with 36 teams
"""

import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Team:
    """Represents a football team"""
    name: str
    country: str
    pot: int
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, Team):
            return self.name == other.name
        return False
    
    def __repr__(self):
        return f"{self.name} ({self.country})"


@dataclass
class DrawConstraints:
    """Draw constraints"""
    matches_per_pot: int = 2
    home_matches: int = 4
    away_matches: int = 4


class ChampionsLeagueDraw:
    """Champions League draw manager"""
    
    def __init__(self, teams: List[Team]):
        self.teams = teams
        self.constraints = DrawConstraints()
        
        self.fixtures: Dict[Team, List[Tuple[Team, bool]]] = {team: [] for team in teams}
        self.opponents_by_pot: Dict[Team, Dict[int, int]] = {
            team: {1: 0, 2: 0, 3: 0, 4: 0} for team in teams
        }
        self.home_away_count: Dict[Team, Dict[str, int]] = {
            team: {'home': 0, 'away': 0} for team in teams
        }
        self.opponents_by_country: Dict[Team, Dict[str, int]] = {
            team: defaultdict(int) for team in teams
        }
        
    def can_play_against(self, team1: Team, team2: Team, is_home: bool) -> bool:
        """Check if two teams can play against each other"""
        
        if team1 == team2:
            return False
        
        # Teams from the same country CANNOT play against each other
        if team1.country == team2.country:
            return False
        
        # Maximum 2 teams from the same country (for different countries)
        if self.opponents_by_country[team1][team2.country] >= 2:
            return False
        if self.opponents_by_country[team2][team1.country] >= 2:
            return False
        
        for opponent, _ in self.fixtures[team1]:
            if opponent == team2:
                return False
        
        if self.opponents_by_pot[team1][team2.pot] >= self.constraints.matches_per_pot:
            return False
        if self.opponents_by_pot[team2][team1.pot] >= self.constraints.matches_per_pot:
            return False
        
        if is_home and self.home_away_count[team1]['home'] >= self.constraints.home_matches:
            return False
        if not is_home and self.home_away_count[team1]['away'] >= self.constraints.away_matches:
            return False
        if not is_home and self.home_away_count[team2]['home'] >= self.constraints.home_matches:
            return False
        if is_home and self.home_away_count[team2]['away'] >= self.constraints.away_matches:
            return False
        
        return True
    
    def add_match(self, team1: Team, team2: Team, team1_home: bool):
        """Add a match between two teams"""
        
        self.fixtures[team1].append((team2, team1_home))
        self.opponents_by_pot[team1][team2.pot] += 1
        self.opponents_by_country[team1][team2.country] += 1
        
        if team1_home:
            self.home_away_count[team1]['home'] += 1
        else:
            self.home_away_count[team1]['away'] += 1
        
        self.fixtures[team2].append((team1, not team1_home))
        self.opponents_by_pot[team2][team1.pot] += 1
        self.opponents_by_country[team2][team1.country] += 1
        
        if team1_home:
            self.home_away_count[team2]['away'] += 1
        else:
            self.home_away_count[team2]['home'] += 1
    
    def perform_draw(self, max_attempts: int = 100) -> bool:
        """
        Perform the draw
        Returns True if successful, False otherwise
        """
        
        for attempt in range(max_attempts):
            self.fixtures = {team: [] for team in self.teams}
            self.opponents_by_pot = {
                team: {1: 0, 2: 0, 3: 0, 4: 0} for team in self.teams
            }
            self.home_away_count = {
                team: {'home': 0, 'away': 0} for team in self.teams
            }
            self.opponents_by_country = {
                team: defaultdict(int) for team in self.teams
            }
            
            success = self._attempt_draw()
            
            if success:
                print(f"Draw successful after {attempt + 1} attempt(s)")
                return True
        
        print(f"Unable to complete draw after {max_attempts} attempts")
        return False
    
    def _attempt_draw(self) -> bool:
        """Attempt a complete draw"""
        
        teams_shuffled = self.teams.copy()
        random.shuffle(teams_shuffled)
        
        for team in teams_shuffled:
            while len(self.fixtures[team]) < 8:
                possible_opponents = []
                
                for pot in [1, 2, 3, 4]:
                    if self.opponents_by_pot[team][pot] < self.constraints.matches_per_pot:
                        pot_teams = [t for t in self.teams if t.pot == pot and t != team]
                        random.shuffle(pot_teams)
                        
                        for opponent in pot_teams:
                            if self.can_play_against(team, opponent, True):
                                possible_opponents.append((opponent, True))
                            elif self.can_play_against(team, opponent, False):
                                possible_opponents.append((opponent, False))
                
                if not possible_opponents:
                    return False
                
                opponent, is_home = random.choice(possible_opponents)
                self.add_match(team, opponent, is_home)
        
        return True
    
    def display_results(self):
        """Display the draw results"""
        
        print("\n" + "="*80)
        print("CHAMPIONS LEAGUE DRAW RESULTS")
        print("="*80 + "\n")
        
        sorted_teams = sorted(self.teams, key=lambda t: (t.pot, t.name))
        
        for team in sorted_teams:
            print(f"\n{team.name} ({team.country}) - Pot {team.pot}")
            print("-" * 60)
            
            home_matches = [f for f in self.fixtures[team] if f[1]]
            away_matches = [f for f in self.fixtures[team] if not f[1]]
            
            print(f"  HOME matches ({len(home_matches)}):")
            for opponent, _ in sorted(home_matches, key=lambda x: x[0].name):
                print(f"    {team.name} vs {opponent.name} ({opponent.country})")
            
            print(f"\n  AWAY matches ({len(away_matches)}):")
            for opponent, _ in sorted(away_matches, key=lambda x: x[0].name):
                print(f"    {opponent.name} vs {team.name} ({opponent.country})")
    
    def display_results_by_pot(self):
        """Display the draw results pot by pot (like real UEFA ceremony)"""
        
        print("\n" + "="*80)
        print("CHAMPIONS LEAGUE DRAW RESULTS - POT BY POT")
        print("="*80)
        
        for pot_num in [1, 2, 3, 4]:
            print(f"\n{'='*80}")
            print(f"POT {pot_num}")
            print(f"{'='*80}")
            
            pot_teams = sorted([t for t in self.teams if t.pot == pot_num], key=lambda t: t.name)
            
            for team in pot_teams:
                print(f"\n{team.name} ({team.country})")
                print("-" * 60)
                
                home_matches = [f for f in self.fixtures[team] if f[1]]
                away_matches = [f for f in self.fixtures[team] if not f[1]]
                
                print(f"  HOME matches ({len(home_matches)}):")
                for opponent, _ in sorted(home_matches, key=lambda x: x[0].name):
                    print(f"    {team.name} vs {opponent.name} ({opponent.country})")
                
                print(f"\n  AWAY matches ({len(away_matches)}):")
                for opponent, _ in sorted(away_matches, key=lambda x: x[0].name):
                    print(f"    {opponent.name} vs {team.name} ({opponent.country})")
                print()
    
    def verify_constraints(self) -> bool:
        """Verify all constraints are met"""
        
        errors = []
        
        for team in self.teams:
            if len(self.fixtures[team]) != 8:
                errors.append(f"{team.name}: {len(self.fixtures[team])} matches instead of 8")
            
            home_count = sum(1 for _, is_home in self.fixtures[team] if is_home)
            away_count = sum(1 for _, is_home in self.fixtures[team] if not is_home)
            
            if home_count != 4:
                errors.append(f"{team.name}: {home_count} home matches instead of 4")
            if away_count != 4:
                errors.append(f"{team.name}: {away_count} away matches instead of 4")
            
            for pot in [1, 2, 3, 4]:
                count = self.opponents_by_pot[team][pot]
                if count != 2:
                    errors.append(f"{team.name}: {count} opponents from pot {pot} instead of 2")
            
            # Check no teams from same country play each other
            for opponent, _ in self.fixtures[team]:
                if opponent.country == team.country:
                    errors.append(f"{team.name} plays against {opponent.name} (same country: {team.country})")
            
            # Check maximum 2 opponents from same country
            for country, count in self.opponents_by_country[team].items():
                if count > 2:
                    errors.append(f"{team.name}: {count} opponents from {country} (max 2)")
        
        if errors:
            print("\nCONSTRAINT VIOLATIONS:")
            for error in errors:
                print(f"  {error}")
            return False
        else:
            print("\nAll constraints satisfied!")
            return True


def create_sample_teams() -> List[Team]:
    """Create sample teams for the draw (2024-2025 season)"""
    
    teams = [
        # Pot 1
        Team("Real Madrid", "ESP", 1),
        Team("Manchester City", "ENG", 1),
        Team("Bayern Munich", "GER", 1),
        Team("PSG", "FRA", 1),
        Team("Liverpool", "ENG", 1),
        Team("Inter Milan", "ITA", 1),
        Team("Borussia Dortmund", "GER", 1),
        Team("RB Leipzig", "GER", 1),
        Team("Barcelona", "ESP", 1),
        
        # Pot 2
        Team("Bayer Leverkusen", "GER", 2),
        Team("Atletico Madrid", "ESP", 2),
        Team("Atalanta", "ITA", 2),
        Team("Juventus", "ITA", 2),
        Team("Benfica", "POR", 2),
        Team("Arsenal", "ENG", 2),
        Team("Club Brugge", "BEL", 2),
        Team("Shakhtar Donetsk", "UKR", 2),
        Team("AC Milan", "ITA", 2),
        
        # Pot 3
        Team("Feyenoord", "NED", 3),
        Team("Sporting CP", "POR", 3),
        Team("PSV Eindhoven", "NED", 3),
        Team("Dinamo Zagreb", "CRO", 3),
        Team("RB Salzburg", "AUT", 3),
        Team("Lille", "FRA", 3),
        Team("Red Star Belgrade", "SRB", 3),
        Team("Young Boys", "SUI", 3),
        Team("Celtic", "SCO", 3),
        
        # Pot 4
        Team("Slovan Bratislava", "SVK", 4),
        Team("Monaco", "FRA", 4),
        Team("Sparta Prague", "CZE", 4),
        Team("Aston Villa", "ENG", 4),
        Team("Bologna", "ITA", 4),
        Team("Girona", "ESP", 4),
        Team("Stuttgart", "GER", 4),
        Team("Sturm Graz", "AUT", 4),
        Team("Brest", "FRA", 4),
    ]
    
    return teams


def main():
    """Main function"""
    
    print("=" * 70)
    print("CHAMPIONS LEAGUE DRAW 2024-2025")
    print("=" * 70 + "\n")
    
    teams = create_sample_teams()
    
    print(f"{len(teams)} teams participating in the draw")
    print(f"Each team plays 8 matches (4 home, 4 away)")
    print(f"2 opponents from each pot")
    print(f"Teams from same country CANNOT play each other")
    print(f"Maximum 2 opponents from any single country\n")
    
    draw = ChampionsLeagueDraw(teams)
    
    print("Starting draw...")
    success = draw.perform_draw(max_attempts=25000)
    
    if success:
        draw.display_results_by_pot()
        
        print("\n" + "="*80)
        print("CONSTRAINT VERIFICATION")
        print("="*80)
        draw.verify_constraints()
    else:
        print("\nDraw failed. Please try again.")


if __name__ == "__main__":
    main()
