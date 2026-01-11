# 🏀 Fantasy Basketball Draft Model - Explained Simply

## What Does This Project Do?

**The Problem:** In fantasy basketball drafts, some players are drafted too early. For example:
- Kawhi Leonard is amazing when he plays, but he misses lots of games
- Someone might draft him at pick #15, but that's too early given his injury risk
- You'd only want to draft him at pick #32 or later (a discount)

**The Solution:** This project calculates:
1. **How good is each player per game?** (Baseline value)
2. **How risky are they?** (Injury risk, games missed, etc.)
3. **What's the lowest pick you should draft them?** (Minimum Draft Value = MDV)
4. **Are they being drafted too early?** (If ADP < MDV, they're a "fade")

## How It Works (Step by Step)

### Step 1: Calculate Baseline Per-Game Value
**Question:** "If this player plays normally, how many fantasy points per game?"

**How:**
- Look at their last 3 years of stats
- Weight recent years more (50% last year, 30% year before, 20% 2 years ago)
- Adjust for expected role changes (if teammate left, they might get more minutes)
- Adjust for age (young players might improve, old players might decline)

**Output:** Each player gets a "baseline rank" (1 = best, 150 = worst)

**Example:** Kawhi might be rank #15 per game (elite!)

---

### Step 2: Calculate Risk Scores
**Question:** "How risky is this player?"

**Four types of risk:**

1. **Injury Risk (0-1)**
   - How many games did they miss last year vs career average?
   - What type of injuries? (chronic knee problems = worse)
   - How old are they? (older = more injury risk)

2. **Availability (Expected Games)**
   - How many games will they play this year?
   - Based on 3-year average of games played

3. **Shutdown Risk (0-1)**
   - Is their team tanking? (bad teams rest players)
   - Are they a franchise player? (less likely to be rested)
   - Is their playoff spot locked? (contending teams rest players late)

4. **Usage Fragility (0-1)**
   - Does their usage rate match their production?
   - If they have high usage but low production, that's fragile

**Output:** Each player gets risk scores (0 = safe, 1 = very risky)

**Example:** Kawhi might have:
- Injury risk: 0.7 (high)
- Expected games: 55 (low)
- Shutdown risk: 0.3 (medium)
- Usage fragility: 0.2 (low)

---

### Step 3: Calculate Risk-Adjusted ADP (RA-ADP)
**Question:** "What should their draft position be, considering risk?"

**How:**
- Start with baseline rank (how good they are per game)
- Multiply by (1 + weighted risk score)
- Higher risk = worse draft position

**Formula:** `RA-ADP = Baseline Rank × (1 + Risk Score × 1.5)`

**Example:**
- Kawhi baseline rank: 15
- Weighted risk: 0.7
- RA-ADP = 15 × (1 + 0.7 × 1.5) = 15 × 2.05 = **30.75** (rounds to 31)

---

### Step 4: Calculate Minimum Draft Value (MDV)
**Question:** "What's the lowest pick where I'd be comfortable drafting this player?"

**How:**
- Start with RA-ADP
- Apply additional discount for:
  - High risk (need more discount)
  - Low expected games (need more discount)
- This gives you the "minimum draft value"

**Example:**
- Kawhi RA-ADP: 31
- High risk (0.7) + low games (55) = need more discount
- MDV = **32** (don't draft before pick 32)

---

### Step 5: Flag Fades
**Question:** "Are players being drafted too early?"

**How:**
- Compare ADP (Average Draft Position - where they're actually being drafted)
- Compare to MDV (where you should draft them)
- If ADP < MDV → **FADE** (being drafted too early, avoid at that cost)

**Example:**
- Kawhi ADP: 25 (people are drafting him at pick 25)
- Kawhi MDV: 32 (you should only draft him at pick 32+)
- **Result: FADE** - Don't draft Kawhi at pick 25, wait until 32+

---

## What Each File Does

### Main Files

**`main.py`**
- The main script you run
- Calls all the other modules in order
- Generates the final report

**`config.py`**
- All the settings and weights
- Fantasy scoring system (how many points for rebounds, assists, etc.)
- Risk weights (how much each risk factor matters)
- Age adjustments, role adjustment caps, etc.

**`requirements.txt`**
- List of Python packages you need to install
- Run `pip install -r requirements.txt`

---

### Data Collection

**`src/data_collector.py`**
- Fetches NBA player data from APIs
- Gets stats, games played, usage rates, etc.
- Calculates fantasy points from raw stats

**`test_data_collection.py`**
- Test script to verify you can fetch data
- Run this first to make sure everything works

---

### Core Calculations

**`src/baseline.py`**
- Calculates baseline per-game value
- Weighted 3-year average
- Role adjustments (usage/minutes changes)
- Age adjustments (growth/decline)

**`src/risk_adjusted_adp.py`**
- Takes baseline rank and risk scores
- Calculates RA-ADP (risk-adjusted draft position)

**`src/minimum_draft_value.py`**
- Calculates MDV (minimum draft value)
- Applies risk and availability discounts

**`src/fade_analysis.py`**
- Compares ADP to MDV
- Flags players as "fades" (overvalued)

---

### Risk Score Modules (Not Built Yet)

**`src/injury_score.py`** - Calculate injury risk
**`src/availability.py`** - Calculate expected games played
**`src/shutdown_risk.py`** - Calculate shutdown/rest risk
**`src/usage_score.py`** - Calculate usage fragility

---

## How to Use This Project

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test Data Collection
```bash
python test_data_collection.py
```
This verifies you can fetch NBA data.

### Step 3: Build It Piece by Piece

**Start with baseline calculation:**
1. Fetch player stats for last 3 years
2. Calculate fantasy points per game
3. Calculate weighted 3-year average
4. Rank players

**Then add risk scores:**
1. Calculate injury risk
2. Calculate expected games
3. Calculate shutdown risk
4. Calculate usage fragility

**Then calculate draft values:**
1. Calculate RA-ADP
2. Calculate MDV
3. Compare to ADP and flag fades

### Step 4: Run the Full Model
```bash
python main.py
```

---

## Example Output

After running, you'd get something like:

| Player | Baseline Rank | Risk Score | MDV | ADP | Fade? |
|--------|---------------|------------|-----|-----|-------|
| Kawhi Leonard | 15 | 0.7 | 32 | 25 | ✅ YES |
| Mikal Bridges | 25 | 0.2 | 18 | 20 | ❌ NO |
| Zion Williamson | 20 | 0.6 | 40 | 35 | ✅ YES |

**Interpretation:**
- **Kawhi**: Elite per-game (rank 15) but high risk → need discount to pick 32. Being drafted at 25 = FADE
- **Mikal**: Good per-game (rank 25), low risk → can draft at 18. Being drafted at 20 = fine
- **Zion**: Good per-game (rank 20) but high risk → need discount to pick 40. Being drafted at 35 = FADE

---

## Key Concepts

### Baseline = "Expected Value If Nothing Weird Happens"
- NOT their ceiling (best case)
- NOT last year's rank (too noisy)
- IS: Weighted average of last 3 years, adjusted for role/age

### Risk = "How Often Does Weird Stuff Happen?"
- Injuries, games missed, shutdowns, usage changes
- Higher risk = need bigger discount

### MDV = "Am I Being Paid Enough for the Risk?"
- If ADP < MDV → You're not getting enough discount → FADE
- If ADP ≥ MDV → You're getting fair value → DRAFT

---

## What's Built vs What's Not

### ✅ Built (Framework/Structure)
- Project structure
- Configuration system
- Baseline calculation framework
- RA-ADP calculation
- MDV calculation
- Fade analysis

### ❌ Not Built Yet (Need Implementation)
- Actual data fetching (framework exists, needs completion)
- Risk score calculations (injury, availability, shutdown, usage)
- Role adjustment logic (how to detect usage/minutes changes)
- Report generation

---

## Next Steps

1. **Understand the flow**: Baseline → Risk → RA-ADP → MDV → Fades
2. **Test data collection**: Make sure you can fetch NBA stats
3. **Build baseline first**: Get weighted 3-year averages working
4. **Add risk scores one by one**: Start with injury risk (easiest)
5. **Test with known players**: Kawhi, Mikal, Zion - do the numbers make sense?

---

## Questions?

- **"Why weighted 3-year average?"** - Smooths out fluke years, recent data matters more
- **"Why conservative role adjustments?"** - Most "breakouts" are small, not huge jumps
- **"Why separate baseline from risk?"** - Kawhi is elite per-game but risky. This lets you model both.
- **"What if I don't have ADP data?"** - You can still calculate MDV and use it to rank players

---

## The Big Picture

**Old approach (wrong):** "Kawhi is risky, don't draft him"
**New approach (right):** "Kawhi is elite per-game (rank 15) but risky, so only draft him at pick 32+"

This model tells you **exactly when** to draft each player, not just "yes" or "no".
