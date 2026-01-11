# Fantasy Basketball Draft Cost Sensitivity Model - Project Guide

## ✅ Feasibility: YES, this is absolutely possible!

This project is very feasible. All the data you need is available through free APIs and web scraping.

## 🎯 Project Approach: Draft Cost Sensitivity (Not "Do Not Draft")

Instead of a binary "Do Not Draft" list, this model calculates:
- **Minimum Draft Value (MDV)**: Lowest pick where you'd draft a player
- **Risk-Adjusted ADP (RA-ADP)**: Baseline rank adjusted by risk
- **Fade Flags**: Players where ADP < MDV (overvalued)

This correctly handles players like Kawhi - elite per-game value but requires ADP discount.

## 📊 Data Sources

### Primary Data Sources:

1. **nba_api (Python Library)** - RECOMMENDED
   - Free, comprehensive NBA stats
   - Player stats, usage rates, minutes, games played
   - Team standings, rosters
   - Installation: `pip install nba_api`
   - Documentation: https://github.com/swar/nba_api

2. **BALLDONTLIE API** (Alternative)
   - Free REST API
   - Player stats and injury data
   - URL: https://nba.balldontlie.io/

3. **Basketball Reference** (Web Scraping)
   - Historical data, injury history
   - Games played, career averages
   - Use `beautifulsoup4` or `pandas.read_html()`

4. **Injury Data**
   - ESPN injury reports (scraping)
   - NBA.com injury reports
   - Historical injury data from Basketball Reference

### What Data You Can Fetch:

✅ **Player Statistics:**
- Per-game fantasy points
- Usage rate
- Minutes per game
- Games played (last year, career average)
- Position
- Age

✅ **Injury Data:**
- Injury history
- Games missed
- Injury types (can be categorized)

✅ **Team Context:**
- Team standings
- Roster changes
- Coaching information
- Playoff status

⚠️ **Challenges:**
- Injury type classification may require manual categorization or NLP
- "Shutdown risk" requires some manual team analysis or heuristics
- Some advanced metrics might need calculation from raw stats

## 📦 Required Libraries

### Core Libraries:
```bash
pip install pandas numpy requests matplotlib seaborn
```

### NBA Data:
```bash
pip install nba_api
```

### Web Scraping (if needed):
```bash
pip install beautifulsoup4 lxml
```

### Optional (for advanced analysis):
```bash
pip install scikit-learn  # For modeling/regression
pip install jupyter       # For interactive analysis
```

## 🏗️ Project Structure

```
fantasy-bball-dnd/
├── main.py                 # Main execution script
├── config.py              # Configuration (weights, thresholds, scoring)
├── data/
│   ├── raw/               # Raw API responses
│   ├── processed/         # Cleaned data
│   └── cache/             # Cached API calls
├── src/
│   ├── data_collector.py  # Fetch data from APIs
│   ├── baseline.py        # Baseline per-game value (3-year weighted + adjustments)
│   ├── role_adjustments.py # Role/usage changes (if needed)
│   ├── age_adjustments.py  # Age curve adjustments (if needed)
│   ├── usage_score.py     # Usage fragility risk
│   ├── injury_score.py    # Injury risk score
│   ├── shutdown_risk.py   # Shutdown/rest risk
│   ├── availability.py    # Expected games played
│   ├── risk_adjusted_adp.py # RA-ADP calculation
│   ├── minimum_draft_value.py # MDV calculation
│   ├── fade_analysis.py   # Flag fades (ADP < MDV)
│   └── utils.py           # Helper functions
├── requirements.txt       # Dependencies
├── PROJECT_GUIDE.md      # This file
└── README.md             # Project overview
```

## 🚀 Getting Started Steps

### Step 1: Setup Environment
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Test Data Collection
```bash
python test_data_collection.py
```
- Verify you can fetch player stats
- Test fantasy points calculation
- Check data structure

### Step 3: Build Incrementally

**Phase 1: Baseline Calculation**
1. **Baseline Per-Game Value**
   - Weighted 3-year average (50% last year, 30% year-1, 20% year-2)
   - Role adjustments (usage/minutes changes) - conservative caps
   - Age curve adjustments (growth/decline)

**Phase 2: Risk Scores**
2. **Injury Score** - Games played trends, injury types, age, recurrence
3. **Availability Score** - Expected games played (3-year smoothed)
4. **Shutdown Risk** - Team context (tanking, contending, playoff certainty)
5. **Usage Fragility** - Usage vs production relationship

**Phase 3: Draft Analysis**
6. **Risk-Adjusted ADP** - Baseline rank × (1 + weighted risk)
7. **Minimum Draft Value (MDV)** - Lowest pick to draft player
8. **Fade Analysis** - Flag players where ADP < MDV

## 📝 Implementation Notes

### Baseline Calculation Philosophy

**Baseline = "What happens if nothing weird happens?"**

- NOT last year's rank (too noisy)
- NOT ceiling projection (too optimistic)
- NOT best-case breakout (not realistic)

**Baseline IS:**
- Weighted 3-year average (smooths fluke years)
- Adjusted for expected role changes (conservative)
- Age-adjusted (growth/decline curves)

### Role Adjustments (Conservative)

**Usage Changes:**
- Cap at ±5% for most players
- Cap at ±8% for young players (≤24)
- Most "breakouts" are +2-4 FPTS, not +10

**Minutes Changes:**
- Cap at ±6 minutes for most players
- Cap at ±8 minutes for young players

**Triggers for Adjustment:**
- Teammates leaving (vacated usage)
- Trades / free agency
- Coaching changes
- Depth chart clarity

### Age Curve Adjustments

- **19-23**: +2% (growth potential)
- **24-27**: 0% (peak, no adjustment)
- **28-30**: -2% (slight decline)
- **31-33**: -5% (moderate decline)
- **34+**: -10% (steep decline)

### Fantasy Points Calculation
Your scoring system is in `config.py`. Adjust based on your league:
- Points, FGM, FGA, 3PM, FTM, FTA, REB, AST, STL, BLK, TOV

### Usage Rate
- Available in `nba_api` player stats
- Or calculate: (FGA + 0.44 * FTA + TO) / Team Plays

### Injury Classification
You may need to manually categorize or use keywords:
- Soft tissue: hamstring, groin, calf, quad
- Chronic: knee, back, ankle
- Fractures: foot, hand, wrist
- Load management: rest, DNP

### Team Context for Shutdown Risk
Heuristics you can implement:
- Tanking teams: Bottom 4 in standings
- Contending teams: Top 11 in conference
- Franchise players: Top 2 usage on team
- Playoff certainty: Games ahead/behind 8th seed

### MDV Calculation Logic

**Example: Kawhi Leonard**
- Baseline rank: 15 (elite per-game)
- Risk score: 0.7 (high)
- Expected games: 55
- MDV: ~32 (need 17 pick discount)

**Example: Mikal Bridges**
- Baseline rank: 25 (good per-game)
- Risk score: 0.2 (low)
- Expected games: 82
- MDV: ~18 (can draft earlier)

High per-game value + high risk = requires ADP discount (higher MDV)

## 🎯 Next Steps

1. **Test data collection** - Run `test_data_collection.py` to verify API access
2. **Build baseline calculation** - Implement weighted 3-year average
3. **Add role adjustments** - Conservative usage/minutes changes
4. **Add age adjustments** - Apply age curve modifiers
5. **Build risk scores** - Injury, availability, shutdown, usage fragility
6. **Calculate RA-ADP** - Apply risk to baseline rank
7. **Calculate MDV** - Determine minimum draft value
8. **Flag fades** - Compare ADP to MDV
9. **Iterate and refine** - Adjust weights and thresholds based on results

## 💡 Key Insights

### Why This Approach Works

1. **Separates baseline from risk** - Kawhi is elite per-game but high risk
2. **Quantifies discount needed** - MDV tells you exactly when to draft
3. **Handles all player types** - Works for ironmen and injury-prone stars
4. **Actionable output** - "Draft Kawhi after pick 32" not just "risky"

### Baseline vs Upside

- **Baseline** = 50th percentile (expected outcome)
- **Upside** = 75-85th percentile (best case)
- **Downside** = 25th percentile (worst case)

Don't bake upside into baseline - that's what risk discount handles.

## 💡 Tips

- Cache API responses to avoid rate limits
- Start with last season's data (2023-24) for testing
- Use pandas DataFrames for all data manipulation
- Create visualizations to validate your scoring (usage vs FPTS graphs)
- Test with known "do not draft" players to validate your model

## 🔗 Useful Resources

- nba_api docs: https://github.com/swar/nba_api
- Basketball Reference: https://www.basketball-reference.com/
- NBA Stats: https://www.nba.com/stats
- Fantasy scoring calculator: Build your own based on your league settings
