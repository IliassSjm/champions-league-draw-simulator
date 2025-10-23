"""
Script to export draw results to JSON format
"""

import json
from champions_league_draw import ChampionsLeagueDraw, create_sample_teams


def export_draw_to_json(draw: ChampionsLeagueDraw, filename: str = "draw_results.json"):
    """Export draw results to JSON"""
    
    results = {
        "tournament": "UEFA Champions League 2024-2025",
        "format": {
            "total_teams": len(draw.teams),
            "matches_per_team": 8,
            "home_matches": 4,
            "away_matches": 4,
            "pots": 4
        },
        "teams": [],
        "matches": []
    }
    
    for team in sorted(draw.teams, key=lambda t: (t.pot, t.name)):
        team_data = {
            "name": team.name,
            "country": team.country,
            "pot": team.pot,
            "fixtures": {
                "home": [],
                "away": []
            }
        }
        
        for opponent, is_home in draw.fixtures[team]:
            match_info = {
                "opponent": opponent.name,
                "opponent_country": opponent.country,
                "opponent_pot": opponent.pot
            }
            
            if is_home:
                team_data["fixtures"]["home"].append(match_info)
            else:
                team_data["fixtures"]["away"].append(match_info)
        
        results["teams"].append(team_data)
    
    matches_set = set()
    for team in draw.teams:
        for opponent, is_home in draw.fixtures[team]:
            if is_home:
                match = (team.name, opponent.name)
                if match not in matches_set and (opponent.name, team.name) not in matches_set:
                    matches_set.add(match)
                    results["matches"].append({
                        "home_team": team.name,
                        "away_team": opponent.name,
                        "home_country": team.country,
                        "away_country": opponent.country
                    })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Results exported to {filename}")
    print(f"  - {len(results['teams'])} teams")
    print(f"  - {len(results['matches'])} unique matches")
    
    return results


def main():
    """Main function"""
    
    print("Generating draw...")
    teams = create_sample_teams()
    draw = ChampionsLeagueDraw(teams)
    
    if draw.perform_draw(max_attempts=1000):
        export_draw_to_json(draw, "ucl_draw_2024_2025.json")
        
        print("\nVerifying constraints...")
        draw.verify_constraints()
    else:
        print("Draw failed")


if __name__ == "__main__":
    main()
