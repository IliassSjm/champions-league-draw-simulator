"""
Sequential Champions League Draw - Pot by Pot
Simulates the real UEFA draw process where teams are drawn pot by pot
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import random


@dataclass(frozen=True)
class Team:
    """Represents a football team"""
    name: str
    country: str
    pot: int


@dataclass
class DrawConstraints:
    """Draw constraints"""
    matches_per_pot: int = 2
    home_matches: int = 4
    away_matches: int = 4


class SequentialChampionsLeagueDraw:
    """
    Sequential draw system - draws pot by pot like real UEFA ceremony
    """
    
    def __init__(self, teams: List[Team], constraints: DrawConstraints = None):
        self.teams = teams
        self.constraints = constraints or DrawConstraints()
        
        # Group teams by pot
        self.teams_by_pot = {1: [], 2: [], 3: [], 4: []}
        for team in teams:
            self.teams_by_pot[team.pot].append(team)
        
        # Results
        self.fixtures = {team: [] for team in teams}
        self.opponents_by_pot = {team: {1: 0, 2: 0, 3: 0, 4: 0} for team in teams}
        self.home_away_count = {team: {'home': 0, 'away': 0} for team in teams}
        self.opponents_by_country = {team: defaultdict(int) for team in teams}
        
        # Current draw state
        self.current_pot = None
        self.current_team = None
        self.draw_history = []
    
    def can_play_against(self, team1: Team, team2: Team, is_home: bool) -> bool:
        """Check if two teams can play against each other"""
        
        if team1 == team2:
            return False
        
        # Same country cannot play
        if team1.country == team2.country:
            return False
        
        # Maximum 2 from same foreign country
        if self.opponents_by_country[team1][team2.country] >= 2:
            return False
        if self.opponents_by_country[team2][team1.country] >= 2:
            return False
        
        # Already played
        for opponent, _ in self.fixtures[team1]:
            if opponent == team2:
                return False
        
        # Pot distribution
        if self.opponents_by_pot[team1][team2.pot] >= self.constraints.matches_per_pot:
            return False
        if self.opponents_by_pot[team2][team1.pot] >= self.constraints.matches_per_pot:
            return False
        
        # Home/away balance
        if is_home:
            if self.home_away_count[team1]['home'] >= self.constraints.home_matches:
                return False
            if self.home_away_count[team2]['away'] >= self.constraints.away_matches:
                return False
        else:
            if self.home_away_count[team1]['away'] >= self.constraints.away_matches:
                return False
            if self.home_away_count[team2]['home'] >= self.constraints.home_matches:
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
        
        # Update opponent
        self.fixtures[team2].append((team1, not team1_home))
        self.opponents_by_pot[team2][team1.pot] += 1
        self.opponents_by_country[team2][team1.country] += 1
        
        if team1_home:
            self.home_away_count[team2]['away'] += 1
        else:
            self.home_away_count[team2]['home'] += 1
    
    def draw_team_opponents(self, team: Team, max_attempts: int = 1000) -> bool:
        """
        Draw all 8 opponents for a specific team
        Returns True if successful
        """
        
        self.current_team = team
        
        for attempt in range(max_attempts):
            # Save state
            saved_fixtures = {t: list(self.fixtures[t]) for t in self.teams}
            saved_opponents_pot = {t: dict(self.opponents_by_pot[t]) for t in self.teams}
            saved_home_away = {t: dict(self.home_away_count[t]) for t in self.teams}
            saved_opponents_country = {t: defaultdict(int, self.opponents_by_country[t]) for t in self.teams}
            
            # Try to draw 8 matches for this team
            success = self._attempt_team_draw(team)
            
            if success:
                return True
            
            # Restore state
            self.fixtures = saved_fixtures
            self.opponents_by_pot = saved_opponents_pot
            self.home_away_count = saved_home_away
            self.opponents_by_country = saved_opponents_country
        
        return False
    
    def _attempt_team_draw(self, team: Team) -> bool:
        """Attempt to draw all opponents for one team"""
        
        initial_matches = len(self.fixtures[team])
        
        while len(self.fixtures[team]) < 8:
            # Find possible opponents
            possible_opponents = []
            
            for pot in [1, 2, 3, 4]:
                if self.opponents_by_pot[team][pot] < self.constraints.matches_per_pot:
                    pot_teams = [t for t in self.teams_by_pot[pot] if t != team]
                    random.shuffle(pot_teams)
                    
                    for opponent in pot_teams:
                        # Skip if opponent already has 8 matches
                        if len(self.fixtures[opponent]) >= 8:
                            continue
                        
                        if self.can_play_against(team, opponent, True):
                            possible_opponents.append((opponent, True))
                        elif self.can_play_against(team, opponent, False):
                            possible_opponents.append((opponent, False))
            
            if not possible_opponents:
                return False
            
            opponent, is_home = random.choice(possible_opponents)
            self.add_match(team, opponent, is_home)
        
        return True
    
    def perform_draw_sequential(self, max_attempts_per_team: int = 5000, max_global_attempts: int = 50) -> bool:
        """
        Perform the draw sequentially, pot by pot
        Returns True if successful
        """
        
        for global_attempt in range(max_global_attempts):
            # Reset everything
            self.fixtures = {team: [] for team in self.teams}
            self.opponents_by_pot = {team: {1: 0, 2: 0, 3: 0, 4: 0} for team in self.teams}
            self.home_away_count = {team: {'home': 0, 'away': 0} for team in self.teams}
            self.opponents_by_country = {team: defaultdict(int) for team in self.teams}
            
            print("\n" + "="*80)
            print(f"STARTING SEQUENTIAL DRAW - ATTEMPT {global_attempt + 1}")
            print("="*80)
            
            all_pots_success = True
            
            # Draw pot by pot
            for pot_number in [1, 2, 3, 4]:
                self.current_pot = pot_number
                print(f"\n{'='*80}")
                print(f"POT {pot_number} DRAW")
                print(f"{'='*80}\n")
                
                teams_in_pot = list(self.teams_by_pot[pot_number])
                random.shuffle(teams_in_pot)
                
                for team in teams_in_pot:
                    print(f"\nDrawing {team.name} ({team.country})...")
                    
                    success = self.draw_team_opponents(team, max_attempts_per_team)
                    
                    if not success:
                        print(f"Failed to draw {team.name}, restarting entire draw...")
                        all_pots_success = False
                        break
                    
                    # Display results for this team immediately
                    self.display_team_result(team)
                
                if not all_pots_success:
                    break
            
            if all_pots_success:
                print(f"\n{'='*80}")
                print("DRAW COMPLETED SUCCESSFULLY!")
                print(f"{'='*80}\n")
                return True
        
        print(f"\nFailed to complete draw after {max_global_attempts} global attempts")
        return False
    
    def display_team_result(self, team: Team):
        """Display the draw result for a single team"""
        
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
        print()
    
    def display_full_results(self):
        """Display complete results"""
        
        print("\n" + "="*80)
        print("COMPLETE DRAW RESULTS")
        print("="*80)
        
        for pot_number in [1, 2, 3, 4]:
            print(f"\n{'='*80}")
            print(f"POT {pot_number}")
            print(f"{'='*80}")
            
            for team in sorted(self.teams_by_pot[pot_number], key=lambda t: t.name):
                self.display_team_result(team)
    
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
            
            # Check same country
            for opponent, _ in self.fixtures[team]:
                if opponent.country == team.country:
                    errors.append(f"{team.name} plays {opponent.name} (same country)")
            
            # Check max 2 from same country
            for country, count in self.opponents_by_country[team].items():
                if count > 2:
                    errors.append(f"{team.name}: {count} opponents from {country} (max 2)")
        
        if errors:
            print("\n" + "="*80)
            print("CONSTRAINT VIOLATIONS")
            print("="*80)
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("\n" + "="*80)
            print("All constraints satisfied!")
            print("="*80)
            return True


def create_sample_teams() -> List[Team]:
    """Create the 36 teams for 2024-2025 format"""
    
    teams_data = [
        # Pot 1
        ("Real Madrid", "ESP", 1), ("Manchester City", "ENG", 1), ("Bayern Munich", "GER", 1),
        ("PSG", "FRA", 1), ("Liverpool", "ENG", 1), ("Inter", "ITA", 1),
        ("Borussia Dortmund", "GER", 1), ("RB Leipzig", "GER", 1), ("Barcelona", "ESP", 1),
        
        # Pot 2
        ("Bayer Leverkusen", "GER", 2), ("Atletico Madrid", "ESP", 2), ("Atalanta", "ITA", 2),
        ("Juventus", "ITA", 2), ("Benfica", "POR", 2), ("Arsenal", "ENG", 2),
        ("Club Brugge", "BEL", 2), ("Shakhtar Donetsk", "UKR", 2), ("AC Milan", "ITA", 2),
        
        # Pot 3
        ("Feyenoord", "NED", 3), ("Sporting CP", "POR", 3), ("PSV", "NED", 3),
        ("Dinamo Zagreb", "CRO", 3), ("Red Bull Salzburg", "AUT", 3), ("Lille", "FRA", 3),
        ("Crvena Zvezda", "SRB", 3), ("Young Boys", "SUI", 3), ("Celtic", "SCO", 3),
        
        # Pot 4
        ("Slovan Bratislava", "SVK", 4), ("Monaco", "FRA", 4), ("Sparta Prague", "CZE", 4),
        ("Aston Villa", "ENG", 4), ("Bologna", "ITA", 4), ("Girona", "ESP", 4),
        ("Stuttgart", "GER", 4), ("Sturm Graz", "AUT", 4), ("Brest", "FRA", 4),
    ]
    
    return [Team(name, country, pot) for name, country, pot in teams_data]


def main():
    """Main function"""
    
    print("\n" + "="*80)
    print("CHAMPIONS LEAGUE DRAW 2024-2025 - SEQUENTIAL")
    print("="*80 + "\n")
    
    teams = create_sample_teams()
    
    print(f"{len(teams)} teams participating in the draw")
    print(f"Each team plays 8 matches (4 home, 4 away)")
    print(f"2 opponents from each pot")
    print(f"Teams from same country CANNOT play each other")
    print(f"Maximum 2 opponents from any single country")
    
    draw = SequentialChampionsLeagueDraw(teams)
    
    success = draw.perform_draw_sequential(max_attempts_per_team=5000)
    
    if success:
        print("\n" + "="*80)
        print("CONSTRAINT VERIFICATION")
        print("="*80)
        draw.verify_constraints()
    else:
        print("\nDraw failed. Please try again.")


if __name__ == "__main__":
    main()

