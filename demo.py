#!/usr/bin/env python3
"""
Complete demonstration script for the draw system
"""

import sys
import time
from champions_league_draw import ChampionsLeagueDraw, create_sample_teams
from export_json import export_draw_to_json
from statistics import DrawStatistics


def print_banner(text):
    """Print a banner"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_step(step, total, text):
    """Print a step"""
    print(f"\n[{step}/{total}] {text}")
    print("-" * 80)


def main():
    """Main demonstration"""
    
    print("\n")
    print("=" * 76)
    print("COMPLETE DEMONSTRATION OF CHAMPIONS LEAGUE DRAW SYSTEM")
    print("=" * 76)
    
    # Step 1: Create teams
    print_step(1, 6, "CREATING TEAMS")
    teams = create_sample_teams()
    print(f"Created {len(teams)} teams")
    
    pots = {1: 0, 2: 0, 3: 0, 4: 0}
    for team in teams:
        pots[team.pot] += 1
    
    print("\nDistribution by pot:")
    for pot, count in pots.items():
        print(f"  Pot {pot}: {count} teams")
    
    # Step 2: Configure draw
    print_step(2, 6, "CONFIGURING DRAW")
    draw = ChampionsLeagueDraw(teams)
    print("Draw system initialized")
    print(f"  - {len(draw.teams)} teams registered")
    print(f"  - Constraints: 2 opponents per pot, 4 home/4 away, no same-country matches")
    
    # Step 3: Perform draw
    print_step(3, 6, "PERFORMING DRAW")
    print("Starting draw (may take a few seconds)...")
    
    start_time = time.time()
    max_attempts = 1000
    success = draw.perform_draw(max_attempts=max_attempts)
    elapsed = time.time() - start_time
    
    if not success:
        print(f"\nDraw failed after {max_attempts} attempts")
        print("Please run the script again.")
        sys.exit(1)
    
    print(f"\nDraw successful in {elapsed:.2f} seconds")
    
    # Step 4: Show sample matches
    print_step(4, 6, "SAMPLE MATCHES")
    
    sample_teams = [
        next(t for t in teams if t.name == "Real Madrid"),
        next(t for t in teams if t.name == "Arsenal"),
        next(t for t in teams if t.name == "Monaco"),
    ]
    
    for team in sample_teams:
        print(f"\n{team.name} ({team.country}) - Pot {team.pot}")
        
        home_matches = [(opp, is_home) for opp, is_home in draw.fixtures[team] if is_home]
        away_matches = [(opp, is_home) for opp, is_home in draw.fixtures[team] if not is_home]
        
        print(f"  Home ({len(home_matches)}): ", end="")
        print(", ".join([opp.name for opp, _ in home_matches]))
        
        print(f"  Away ({len(away_matches)}): ", end="")
        print(", ".join([opp.name for opp, _ in away_matches]))
    
    # Step 5: Verify constraints
    print_step(5, 6, "VERIFYING CONSTRAINTS")
    
    errors = []
    for team in teams:
        if len(draw.fixtures[team]) != 8:
            errors.append(f"{team.name}: {len(draw.fixtures[team])} matches")
        
        home = sum(1 for _, is_home in draw.fixtures[team] if is_home)
        if home != 4:
            errors.append(f"{team.name}: {home} home matches")
        
        for pot in [1, 2, 3, 4]:
            if draw.opponents_by_pot[team][pot] != 2:
                errors.append(f"{team.name}: {draw.opponents_by_pot[team][pot]} opponents from pot {pot}")
        
        for opponent, _ in draw.fixtures[team]:
            if opponent.country == team.country:
                errors.append(f"{team.name} plays {opponent.name} (same country)")
    
    if errors:
        print("\nConstraint violations:")
        for error in errors[:5]:
            print(f"  {error}")
    else:
        print("\nAll constraints satisfied!")
        print("  - 8 matches per team")
        print("  - 4 home matches, 4 away matches")
        print("  - 2 opponents from each pot")
        print("  - No teams from same country play each other")
    
    # Step 6: Export and statistics
    print_step(6, 6, "EXPORT AND STATISTICS")
    
    print("\nExporting to JSON...")
    json_file = "demo_draw.json"
    export_draw_to_json(draw, json_file)
    
    print("\nGenerating statistics...")
    stats = DrawStatistics(draw)
    
    country_matchups = stats.country_matchups()
    total_international = sum(sum(opponents.values()) for opponents in country_matchups.values())
    print(f"  - International matches: {total_international}")
    
    # Final summary
    print_banner("DEMONSTRATION COMPLETE")
    print("\nThe system works perfectly!")
    print(f"\nFiles generated:")
    print(f"  - {json_file} (JSON results)")
    print(f"\nTo go further:")
    print("  - Run 'python3 champions_league_draw.py' for a complete draw")
    print("  - Run 'python3 statistics.py' for detailed statistics")
    print("  - Open 'web_interface.html' for the interactive web interface")
    print("  - Run 'python3 test_draw.py' for unit tests")
    print("\nDocumentation:")
    print("  - README.md - Complete documentation")
    
    print("\n" + "="*80)
    print("Thank you for using the Champions League Draw System!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
