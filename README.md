# Fantasy Basketball Draft Cost Sensitivity Model

A data-driven tool to calculate **Minimum Draft Value (MDV)** and identify players who are overvalued in fantasy basketball drafts. Instead of a binary "Do Not Draft" list, this model tells you exactly when to draft each player based on their risk-adjusted value.

## 🎯 Project Goal

Calculate draft cost sensitivity for players by analyzing:
- **Baseline Per-Game Value**: Weighted 3-year average + role/age adjustments
- **Risk Scores**: Injury, availability, shutdown, usage fragility
- **Risk-Adjusted ADP (RA-ADP)**: Baseline rank adjusted by risk
- **Minimum Draft Value (MDV)**: Lowest pick where player becomes draftable
- **Fade Flags**: Players where ADP < MDV (overvalued)

This correctly handles players like Kawhi Leonard - elite per-game value but requires significant ADP discount.

## 📋 Methodology

### Phase 1: Baseline Calculation
1. **Weighted 3-Year Average**: 50% last year, 30% year-1, 20% year-2
2. **Role Adjustments**: Conservative usage/minutes changes based on team context
3. **Age Curve Adjustments**: Growth/decline modifiers by age bucket

### Phase 2: Risk Scoring
4. **Injury Score (0-1)**: Games played trends, injury types, age, recurrence
5. **Availability Score**: Expected games played (3-year smoothed)
6. **Shutdown Risk (0-1)**: Team context (tanking, contending, playoff certainty)
7. **Usage Fragility (0-1)**: Usage vs production relationship

### Phase 3: Draft Analysis
8. **Risk-Adjusted ADP**: Baseline rank × (1 + weighted risk score)
9. **Minimum Draft Value**: Calculated from RA-ADP, risk, and expected games
10. **Fade Analysis**: Flag players where ADP < MDV

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## 📁 Project Structure

```
fantasy-bball-dnd/
├── main.py                 # Main execution script
├── config.py              # Configuration (weights, thresholds, scoring)
├── requirements.txt       # Python dependencies
├── test_data_collection.py # Test script for data fetching
├── src/
│   ├── data_collector.py  # Fetch NBA data from APIs
│   ├── baseline.py        # Baseline per-game value (3-year weighted)
│   ├── risk_adjusted_adp.py # RA-ADP calculation
│   ├── minimum_draft_value.py # MDV calculation
│   ├── fade_analysis.py   # Fade flagging (ADP < MDV)
│   ├── usage_score.py     # Usage fragility risk
│   ├── injury_score.py    # Injury risk scoring
│   ├── shutdown_risk.py   # Shutdown/rest risk
│   └── availability.py    # Expected games played
└── data/                  # Data storage (create this)
    ├── raw/              # Raw API responses
    ├── processed/        # Cleaned data
    └── cache/           # Cached data
```

## 📊 Data Sources

- **nba_api**: Player statistics, usage rates, games played
- **Basketball Reference**: Historical data, injury history
- **NBA.com**: Team standings, roster information

## ⚙️ Configuration

Edit `config.py` to adjust:
- **Fantasy scoring**: Match your league settings (points, rebounds, assists, etc.)
- **Baseline weights**: 3-year average weighting
- **Role adjustment caps**: Conservative limits for usage/minutes changes
- **Age modifiers**: Growth/decline curves by age bucket
- **Risk weights**: How much each risk factor affects RA-ADP
- **MDV calculation**: Risk discount factors and minimum games threshold

## 🔧 Development Status

- [x] Project structure
- [x] Configuration setup
- [x] Baseline calculation framework
- [x] RA-ADP calculation framework
- [x] MDV calculation framework
- [x] Fade analysis framework
- [ ] Data collection implementation
- [ ] Role adjustment logic
- [ ] Risk score implementations
- [ ] Report generation

## 📝 Notes

See `PROJECT_GUIDE.md` for detailed implementation notes and data source information.

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

MIT
