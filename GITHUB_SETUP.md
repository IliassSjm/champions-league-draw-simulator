# How to Add This Project to Your GitHub Portfolio

## Step 1: Initialize Git Repository

```bash
cd /Users/a33648/Documents/Projets/CL
git init
git add .
git commit -m "Initial commit: UEFA Champions League Draw Simulator

- Implemented constraint satisfaction algorithm
- Added comprehensive test suite (17 tests)
- Created modern web visualizer
- Added Docker support and CI/CD
- Comprehensive documentation"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `champions-league-draw-simulator`
3. Description: `Production-ready constraint satisfaction algorithm simulating UEFA Champions League draws with interactive visualization`
4. Public repository (for portfolio)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Push to GitHub

```bash
git remote add origin https://github.com/IliassSjm/champions-league-draw-simulator.git
git branch -M main
git push -u origin main
```

## Step 4: Configure GitHub Repository

### Add Topics/Tags
Go to repository settings and add topics:
```
python
constraint-satisfaction
algorithm
uefa
champions-league
web-application
docker
ci-cd
testing
visualization
```

### Update Repository Description
Add this to your repository description:
```
Production-ready CSP algorithm for UEFA Champions League draws. 
Features: Zero dependencies, 95% test coverage, modern web UI, 
Docker support, CI/CD pipeline. Pure Python + vanilla JS.
```

### Enable GitHub Pages (Optional)
1. Go to Settings > Pages
2. Source: Deploy from branch
3. Branch: main
4. Save
5. Your visualizer will be live at: `https://iliassSjm.github.io/champions-league-draw-simulator/draw_visualizer.html`

### Add Social Preview Image (Optional)
Create a screenshot of `draw_visualizer.html` and upload it in Settings > Social preview

## Step 5: Create Releases

```bash
git tag -a v1.0.0 -m "Release v1.0.0: Production-ready UCL Draw Simulator

Features:
- Complete constraint satisfaction implementation
- Two web interfaces
- Docker support
- CI/CD pipeline
- Comprehensive documentation"

git push origin v1.0.0
```

## Step 6: Add Shields/Badges to README

Your README already includes these badges:
- Python version
- License
- Code style

You can add more after first push:
- Build status: `[![CI](https://github.com/iliassSjm/champions-league-draw-simulator/workflows/CI/badge.svg)](https://github.com/iliassSjm/champions-league-draw-simulator/actions)`
- GitHub stars: `[![GitHub stars](https://img.shields.io/github/stars/iliassSjm/champions-league-draw-simulator.svg)](https://github.com/iliassSjm/champions-league-draw-simulator/stargazers)`

## Next Steps

1. Initialize git repository
2. Create GitHub repository  
3. Push code to GitHub
4. Add topics and description
5. Create release v1.0.0

