# Contributing to Champions League Draw Simulator

First off, thank you for considering contributing to this project!

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Description**: Clear and concise description of the bug
- **Steps to Reproduce**: Step-by-step reproduction
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, OS, browser (if web interface)
- **Screenshots**: If applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title** describing the enhancement
- **Provide detailed description** of the suggested enhancement
- **Explain why** this enhancement would be useful
- **List alternatives** you've considered

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`python test_draw.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Guidelines

### Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add type hints where appropriate

```python
def good_function(team: Team, opponent: Team) -> bool:
    """
    Check if two teams can play against each other.
    
    Args:
        team: The first team
        opponent: The opposing team
    
    Returns:
        True if match is valid, False otherwise
    """
    return team.country != opponent.country
```

### Testing

- Add tests for new features
- Ensure all existing tests pass
- Aim for high test coverage
- Test edge cases

```python
def test_new_feature(self):
    """Test the new feature works correctly"""
    # Arrange
    team = Team("Test Team", "TST", 1)
    
    # Act
    result = new_feature(team)
    
    # Assert
    self.assertEqual(result, expected_value)
```

### Commit Messages

Use clear and descriptive commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes
- **refactor**: Code refactoring
- **test**: Test additions/changes
- **chore**: Build process or auxiliary tool changes

Examples:
```
feat: add visualization for country distribution
fix: resolve issue with same-country constraint
docs: update README with new features
test: add tests for country limitation
```

### Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Add inline comments for complex logic
- Update docstrings when changing function signatures

## Project Structure

```
champions-league-draw/
├── champions_league_draw.py  # Core algorithm
├── test_draw.py              # Unit tests
├── statistics.py             # Analysis module
├── export_json.py            # Export functionality
├── demo.py                   # Demo script
├── draw_visualizer.html      # Web visualizer
├── web_interface.html        # Alternative interface
├── README.md                 # User documentation
├── ARCHITECTURE.md           # Technical documentation
└── CONTRIBUTING.md           # This file
```

## Adding New Features

### Example: Adding a New Constraint

1. **Update the data model** in `ChampionsLeagueDraw.__init__()`:
```python
self.new_constraint_tracker = {}
```

2. **Add validation** in `can_play_against()`:
```python
if not self.check_new_constraint(team1, team2):
    return False
```

3. **Update tracking** in `add_match()`:
```python
self.new_constraint_tracker[team].update()
```

4. **Add verification** in `verify_constraints()`:
```python
if not self.verify_new_constraint(team):
    errors.append(f"New constraint violated for {team.name}")
```

5. **Add tests** in `test_draw.py`:
```python
def test_new_constraint(self):
    """Test that new constraint is enforced"""
    # Test implementation
```

6. **Update documentation**

## Questions?

Feel free to open an issue with the `question` label.

## Recognition

Contributors will be recognized in the README.md file.

Thank you for contributing!

