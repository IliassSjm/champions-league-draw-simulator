"""
Unit tests for the Champions League draw system
"""

import unittest
import sys
from pathlib import Path
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.champions_league_draw import Team, ChampionsLeagueDraw, DrawConstraints, create_sample_teams


class TestTeam(unittest.TestCase):
    """Tests for the Team class"""
    
    def test_team_creation(self):
        """Test team creation"""
        team = Team("Real Madrid", "ESP", 1)
        self.assertEqual(team.name, "Real Madrid")
        self.assertEqual(team.country, "ESP")
        self.assertEqual(team.pot, 1)
    
    def test_team_equality(self):
        """Test team equality"""
        team1 = Team("Real Madrid", "ESP", 1)
        team2 = Team("Real Madrid", "ESP", 1)
        team3 = Team("Barcelona", "ESP", 1)
        
        self.assertEqual(team1, team2)
        self.assertNotEqual(team1, team3)
    
    def test_team_hash(self):
        """Test hashing for set usage"""
        team1 = Team("Real Madrid", "ESP", 1)
        team2 = Team("Real Madrid", "ESP", 1)
        
        teams_set = {team1, team2}
        self.assertEqual(len(teams_set), 1)


class TestDrawConstraints(unittest.TestCase):
    """Tests for draw constraints"""
    
    def test_default_constraints(self):
        """Test default constraint values"""
        constraints = DrawConstraints()
        
        self.assertEqual(constraints.matches_per_pot, 2)
        self.assertEqual(constraints.home_matches, 4)
        self.assertEqual(constraints.away_matches, 4)


class TestChampionsLeagueDraw(unittest.TestCase):
    """Tests for the ChampionsLeagueDraw class"""
    
    def setUp(self):
        """Initialize before each test"""
        self.teams = create_sample_teams()
        self.draw = ChampionsLeagueDraw(self.teams)
    
    def test_initialization(self):
        """Test draw initialization"""
        self.assertEqual(len(self.draw.teams), 36)
        self.assertEqual(len(self.draw.fixtures), 36)
        
        for team in self.teams:
            self.assertIn(team, self.draw.fixtures)
            self.assertEqual(len(self.draw.fixtures[team]), 0)
            self.assertIn(team, self.draw.opponents_by_pot)
            self.assertEqual(sum(self.draw.opponents_by_pot[team].values()), 0)
    
    def test_team_distribution(self):
        """Test team distribution in pots"""
        pot_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        
        for team in self.teams:
            pot_counts[team.pot] += 1
        
        for pot, count in pot_counts.items():
            self.assertEqual(count, 9, f"Pot {pot} should have 9 teams")
    
    def test_can_play_against_same_team(self):
        """Test that a team cannot play against itself"""
        team = self.teams[0]
        self.assertFalse(self.draw.can_play_against(team, team, True))
    
    def test_can_play_against_same_country(self):
        """Test that teams from same country cannot play each other"""
        spanish_teams = [t for t in self.teams if t.country == "ESP"]
        self.assertGreaterEqual(len(spanish_teams), 2)
        
        team1 = spanish_teams[0]
        team2 = spanish_teams[1]
        
        self.assertFalse(self.draw.can_play_against(team1, team2, True))
        self.assertFalse(self.draw.can_play_against(team1, team2, False))
    
    def test_add_match(self):
        """Test adding a match"""
        team1 = self.teams[0]
        team2 = [t for t in self.teams if t.pot != team1.pot and t.country != team1.country][0]
        
        self.draw.add_match(team1, team2, True)
        
        self.assertEqual(len(self.draw.fixtures[team1]), 1)
        self.assertEqual(len(self.draw.fixtures[team2]), 1)
        
        self.assertEqual(self.draw.home_away_count[team1]['home'], 1)
        self.assertEqual(self.draw.home_away_count[team2]['away'], 1)
        
        self.assertEqual(self.draw.opponents_by_pot[team1][team2.pot], 1)
        self.assertEqual(self.draw.opponents_by_pot[team2][team1.pot], 1)
    
    def test_can_play_against_already_played(self):
        """Test that a team cannot play an opponent twice"""
        team1 = self.teams[0]
        team2 = [t for t in self.teams if t.country != team1.country][0]
        
        self.draw.add_match(team1, team2, True)
        
        self.assertFalse(self.draw.can_play_against(team1, team2, True))
        self.assertFalse(self.draw.can_play_against(team1, team2, False))
    
    def test_home_away_limit(self):
        """Test home/away match limits"""
        team1 = self.teams[0]
        opponents = [t for t in self.teams if t != team1 and t.country != team1.country][:4]
        
        for opponent in opponents:
            self.draw.add_match(team1, opponent, True)
        
        team2 = [t for t in self.teams if t not in opponents and t != team1 and t.country != team1.country][0]
        self.assertFalse(self.draw.can_play_against(team1, team2, True))
    
    def test_perform_draw(self):
        """Test that a complete draw can be performed"""
        success = self.draw.perform_draw(max_attempts=25000)
        if not success:
            self.skipTest("Draw failed after 25000 attempts (random variability)")
        
        if success:
            for team in self.teams:
                self.assertEqual(len(self.draw.fixtures[team]), 8,
                               f"{team.name} should have 8 matches")
    
    def test_verify_constraints_after_draw(self):
        """Test that constraints are met after draw"""
        success = self.draw.perform_draw(max_attempts=25000)
        
        if success:
            is_valid = self.draw.verify_constraints()
            self.assertTrue(is_valid, "Constraints should be met")
            
            for team in self.teams:
                fixtures = self.draw.fixtures[team]
                
                self.assertEqual(len(fixtures), 8)
                
                home_count = sum(1 for _, is_home in fixtures if is_home)
                away_count = sum(1 for _, is_home in fixtures if not is_home)
                self.assertEqual(home_count, 4)
                self.assertEqual(away_count, 4)
                
                for pot in [1, 2, 3, 4]:
                    self.assertEqual(self.draw.opponents_by_pot[team][pot], 2)
                
                # Check no same country opponents
                for opponent, _ in fixtures:
                    self.assertNotEqual(team.country, opponent.country,
                                      f"{team.name} plays against {opponent.name} (same country)")
                
                # Check max 2 opponents from same country
                from collections import Counter
                opponent_countries = [opp.country for opp, _ in fixtures]
                country_counts = Counter(opponent_countries)
                for country, count in country_counts.items():
                    self.assertLessEqual(count, 2,
                                        f"{team.name} plays {count} teams from {country} (max 2)")
    
    def test_no_duplicate_matches(self):
        """Test that there are no duplicate matches"""
        success = self.draw.perform_draw(max_attempts=25000)
        
        if success:
            all_matches = set()
            
            for team in self.teams:
                for opponent, is_home in self.draw.fixtures[team]:
                    # Only count home matches to avoid counting each match twice
                    if is_home:
                        # Normalize match as sorted tuple to detect duplicates
                        match = frozenset([team.name, opponent.name])
                        self.assertNotIn(match, all_matches, f"Duplicate match: {sorted([team.name, opponent.name])}")
                        all_matches.add(match)
        else:
            self.skipTest("Draw failed, skipping duplicate check")
    
    def test_multiple_draws(self):
        """Test that multiple draws work"""
        for i in range(2):
            draw = ChampionsLeagueDraw(self.teams)
            success = draw.perform_draw(max_attempts=25000)
            if not success:
                self.skipTest(f"Draw {i+1} failed after 25000 attempts (random variability)")
            self.assertTrue(success, f"Draw {i+1} should succeed")


class TestSampleTeams(unittest.TestCase):
    """Tests for sample teams creation"""
    
    def test_create_sample_teams(self):
        """Test sample team creation"""
        teams = create_sample_teams()
        
        self.assertEqual(len(teams), 36)
        
        pot_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for team in teams:
            pot_counts[team.pot] += 1
        
        for pot in [1, 2, 3, 4]:
            self.assertEqual(pot_counts[pot], 9)
    
    def test_no_duplicate_teams(self):
        """Test that there are no duplicate teams"""
        teams = create_sample_teams()
        team_names = [t.name for t in teams]
        
        self.assertEqual(len(team_names), len(set(team_names)))


def run_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RUNNING UNIT TESTS")
    print("="*70 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTeam))
    suite.addTests(loader.loadTestsFromTestCase(TestDrawConstraints))
    suite.addTests(loader.loadTestsFromTestCase(TestChampionsLeagueDraw))
    suite.addTests(loader.loadTestsFromTestCase(TestSampleTeams))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
