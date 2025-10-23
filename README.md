# UEFA Champions League Draw Simulator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/code%20style-clean-brightgreen.svg)](https://github.com/psf/black)

A sophisticated draw simulation system for the UEFA Champions League 2024-2025 format, featuring advanced constraint satisfaction algorithms and interactive visualizations.

## Project Overview

This project implements the complex UEFA Champions League draw system with all official constraints, demonstrating:
- **Algorithm Design**: Constraint satisfaction with randomized search
- **Web Development**: Modern, responsive interfaces with vanilla JavaScript
- **Software Engineering**: Clean architecture, comprehensive testing, zero external dependencies
- **Data Visualization**: Multiple view modes for result analysis

### Live Demo
[Open Interactive Visualizer](web/draw_visualizer.html) (Download and open in browser)

## Technical Highlights

### Core Algorithm
- **Constraint Satisfaction Problem (CSP)** with randomized backtracking
- Handles 5 simultaneous constraints across 36 teams
- Average complexity: O(n × attempts) where n = 36
- Success rate: >95% within 5000 attempts

### Constraints Implemented
1. **Pot Distribution**: Each team faces exactly 2 opponents from each pot
2. **Home/Away Balance**: Exactly 4 home and 4 away matches per team
3. **Country Exclusion**: Teams from same country cannot play each other
4. **Country Limitation**: Maximum 2 opponents from any single foreign country
5. **Uniqueness**: No duplicate fixtures

### Architecture

```
champions-league-draw/
├── src/
│   ├── champions_league_draw.py  # Core algorithm
│   ├── statistics.py              # Statistical analysis
│   ├── export_json.py             # JSON export
│   └── demo.py                    # Demonstration
├── tests/
│   └── test_draw.py               # Unit tests (17 tests)
├── web/
│   ├── draw_visualizer.html       # Interactive visualizer
│   └── web_interface.html         # Alternative interface
└── docs/                          # Documentation
```

## Features

### 1. Interactive Web Visualizer
- **Grid View**: Visual cards for each team with color-coded pots
- **Table View**: Organized display by pot for comparison
- **Real-time Generation**: Client-side draw execution
- **Export Functionality**: Download results as text file

### 2. Command-Line Interface
```bash
# Run complete draw with verification
python3 -m src.champions_league_draw

# View detailed statistics
python3 -m src.statistics

# Export to JSON format
python3 -m src.export_json

# Run comprehensive demo
python3 -m src.demo
```

### 3. Programmatic API
```python
from src.champions_league_draw import ChampionsLeagueDraw, create_sample_teams

teams = create_sample_teams()
draw = ChampionsLeagueDraw(teams)

if draw.perform_draw(max_attempts=5000):
    draw.display_results()
    draw.verify_constraints()
```

## Installation & Usage

### Prerequisites
- Python 3.10 or higher
- Modern web browser (for visualizer)
- No external dependencies required

### Quick Start

```bash
# Clone the repository
git clone https://github.com/iliassSjm/champions-league-draw.git
cd champions-league-draw

# Run the main program
python3 -m src.champions_league_draw

# Or open the web visualizer
open web/draw_visualizer.html
```

### Running Tests

```bash
# Execute test suite
python3 -m unittest discover -s tests

# Expected output: 17 tests passed
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Draw Time | 1-3 seconds |
| Success Rate | >95% |
| Average Attempts | 300-800 |
| Test Coverage | ~95% |
| Lines of Code | ~2,500 |

## Docker Support

```bash
# Build the image
docker build -t ucl-draw .

# Run the container
docker run -p 8000:8000 ucl-draw
```

## Technical Stack

- **Language**: Python 3.10+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Testing**: unittest (Python standard library)
- **Architecture**: Object-oriented design with separation of concerns
- **Data Structures**: Hash maps for O(1) constraint checking

## Algorithm Explanation

The draw system uses a **randomized constraint satisfaction algorithm**:

1. **Initialization**: Create data structures for all constraints
2. **Random Ordering**: Shuffle team processing order
3. **Greedy Assignment**: For each team, select valid opponents
4. **Constraint Checking**: Verify all rules before assignment
5. **Backtracking**: Restart if no valid assignment exists

### Why This Approach?

- **Simplicity**: Easy to understand and maintain
- **Effectiveness**: High success rate despite complexity
- **Scalability**: Can handle constraint additions
- **Transparency**: Clear verification of all rules

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- UEFA for the Champions League format specifications
- Python community for excellent standard library
- Inspired by the complexity of real-world scheduling problems

---

**Note**: This is an educational project and is not affiliated with UEFA.

Built with attention to detail and clean code principles.
