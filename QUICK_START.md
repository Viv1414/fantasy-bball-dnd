# 🚀 Quick Start Guide

## What This Project Does (30 Second Version)

Calculates **Minimum Draft Value (MDV)** for fantasy basketball players.

**Example:** Kawhi Leonard is amazing per-game (rank #15) but risky. This model says: "Only draft him at pick #32 or later." If he's being drafted at #25, that's a **FADE** (too early).

## The Flow (5 Steps)

```
1. Baseline Value → How good per game? (rank 1-150)
2. Risk Scores → How risky? (0-1 scale)
3. RA-ADP → Risk-adjusted draft position
4. MDV → Minimum pick to draft them
5. Fade Flags → ADP < MDV? (overvalued)
```

## Files You Need to Know

| File | What It Does |
|------|-------------|
| `main.py` | Run this to execute everything |
| `config.py` | All settings (scoring, weights, etc.) |
| `EXPLAINED.md` | **READ THIS FIRST** - Full explanation |
| `test_data_collection.py` | Test if you can fetch NBA data |

## Getting Started (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Data Collection
```bash
python test_data_collection.py
```
Should print: "✅ All tests passed!"

### 3. Read the Full Explanation
```bash
# Open EXPLAINED.md in your editor
# It explains everything in simple terms
```

## What's Working vs What's Not

### ✅ Framework Built
- Project structure
- Configuration system
- Calculation frameworks (baseline, RA-ADP, MDV, fades)

### ❌ Needs Implementation
- Actual data fetching (structure exists, needs completion)
- Risk score calculations (injury, availability, shutdown, usage)
- Role adjustment detection (how to find usage/minutes changes)

## Next Steps

1. **Read `EXPLAINED.md`** - Understand what everything does
2. **Run `test_data_collection.py`** - Verify data access works
3. **Start building baseline** - Implement weighted 3-year average
4. **Add risk scores** - Start with injury risk (easiest)

## Key Concepts

- **Baseline** = Expected per-game value (not ceiling, not last year)
- **Risk** = How often bad stuff happens (injuries, games missed)
- **MDV** = Lowest pick where you'd draft them
- **Fade** = Being drafted too early (ADP < MDV)

## Example Output

```
Player          Baseline  Risk  MDV  ADP  Fade?
Kawhi Leonard   15        0.7   32   25   ✅ YES
Mikal Bridges   25        0.2   18   20   ❌ NO
```

**Translation:**
- Kawhi: Elite (rank 15) but risky → need discount to pick 32. Drafted at 25 = FADE
- Mikal: Good (rank 25), safe → can draft at 18. Drafted at 20 = fine

## Questions?

Read `EXPLAINED.md` - it has detailed explanations of everything!
