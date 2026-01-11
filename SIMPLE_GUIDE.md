# Simple Guide - Everything in 2 Files

## File Structure

1. **`config.py`** - All your settings (scoring, weights, etc.)
2. **`main.py`** - All the code in one place!

## How to Use

### 1. Edit Settings
Open `config.py` and adjust:
- `FANTASY_SCORING` - Match your league scoring
- `BASELINE_WEIGHTS` - How much to weight each year
- `RISK_WEIGHTS` - How much each risk factor matters
- `AGE_MODIFIERS` - Age adjustments

### 2. Run the Code
```bash
python main.py
```

### 3. Build It Yourself
The code is organized into sections:
- **Step 1: Data Collection** - Fetch NBA stats
- **Step 2: Baseline Calculation** - Calculate per-game value
- **Step 3: Risk Scores** - Calculate risk (injury, availability, etc.)
- **Step 4: RA-ADP** - Risk-adjusted draft position
- **Step 5: MDV** - Minimum draft value
- **Step 6: Fade Analysis** - Flag overvalued players

## What's Implemented vs What's TODO

### ✅ Implemented
- Data fetching from nba_api
- Fantasy points calculation
- Weighted 3-year baseline average
- Age adjustments
- Basic injury risk (games played trend)
- Expected games calculation
- RA-ADP calculation
- MDV calculation
- Fade flagging

### ❌ TODO (You Can Build These!)
- **Shutdown risk** - Analyze team context (tanking, contending)
- **Usage fragility** - Analyze usage rate vs production
- **Role adjustments** - Detect usage/minutes changes from team changes
- **Injury type classification** - Categorize injuries (soft tissue, chronic, etc.)
- **ADP data** - Get actual ADP from your draft platform

## How to Build Each Part

### Shutdown Risk
```python
def calculate_shutdown_risk(player_id):
    # 1. Get player's team
    # 2. Get team standings (tanking = bottom 4, contending = top 11)
    # 3. Check if franchise player (top 2 usage on team)
    # 4. Return risk score (0-1)
```

### Usage Fragility
```python
def calculate_usage_fragility(player_id, seasons):
    # 1. Get usage rate for each season
    # 2. Get fantasy points per game
    # 3. Calculate correlation: high usage but low FPTS = fragile
    # 4. Return fragility score (0-1)
```

### Role Adjustments
```python
def apply_role_adjustments(baseline_df):
    # 1. Detect team changes (trades, free agency)
    # 2. Estimate usage/minutes changes
    # 3. Apply conservative caps (±5% usage, ±6 minutes)
    # 4. Adjust baseline FPTS
```

## Tips

1. **Start small** - Test with 5-10 players first
2. **Add one feature at a time** - Don't try to build everything at once
3. **Test with known players** - Kawhi (high risk), Mikal (low risk)
4. **Adjust weights** - Tweak config.py to match your intuition
5. **Add print statements** - See what's happening at each step

## Example: Testing One Player

```python
# Test with Kawhi Leonard
from nba_api.stats.static import players

all_players = players.get_players()
kawhi = [p for p in all_players if p['full_name'] == 'LeBron James'][0]  # Example

# Calculate baseline
baseline = calculate_weighted_3year_average(
    kawhi['id'], 
    ['2023-24', '2022-23', '2021-22'],
    FANTASY_SCORING
)
print(f"Baseline FPTS: {baseline}")

# Calculate risk
risk = calculate_injury_score(kawhi['id'], ['2023-24', '2022-23', '2021-22'])
print(f"Injury Risk: {risk}")
```

## The Flow (Simple Version)

```
1. Get player stats → Calculate fantasy points per game
2. Weight last 3 years → Get baseline value
3. Adjust for age → Young players improve, old decline
4. Calculate risk → Injury, games missed, etc.
5. Apply risk to baseline → Get RA-ADP
6. Calculate MDV → Lowest pick to draft
7. Compare to ADP → Flag fades
```

That's it! Everything is in `main.py` - just build it piece by piece.
