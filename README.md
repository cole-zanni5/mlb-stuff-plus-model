# MLB Stuff+ Model

A pitch quality model built in Python using 2025 MLB Statcast data, designed to replicate the methodology behind Stuff+ metrics seen on sites like FanGraphs.

---

## Overview

Stuff+ is a pitch quality metric that evaluates how good a pitch is based purely on its physical characteristics, independent of outcomes like contact or hits. A score of 100 represents league average for a given pitch type, with every point above or below representing a percentage better or worse than average. This project builds a Stuff+ model from scratch using Statcast pitch tracking data and gradient boosting machine learning, with the goal of producing an analytical tool that can evaluate individual pitches, pitcher arsenals, and pitch quality trends across the 2025 MLB season.

<!-- This project was built as a portfolio piece in pursuit of a career in MLB analytics. -->

---

## Data

All data was sourced from Baseball Savant via the pybaseball Python library.

**Training data:** 2022, 2023, and 2024 MLB regular seasons (~2.1 million pitches). The model weights were established on this historical dataset to give the model sufficient variation to learn what separates elite pitch profiles from average ones.

**Scoring data:** 2025 MLB regular season only (707,343 pitches, March 27 through September 28). All Stuff+ scores reflect 2025 pitch characteristics run through the historically trained model, consistent with how public Stuff+ models operate.

Pitch types with insufficient data or unreliable classifications were removed before training. The 13 retained pitch types are FF, SI, FC, SL, ST, CU, CH, KC, FS, SV, CS, KN, and FO.

---

## Methodology

**Features**

Each pitch is described by the following Statcast tracked physical characteristics:

- Release speed
- Release spin rate
- Induced vertical break (pfx_z)
- Horizontal break (pfx_x)
- Release extension
- Release position (horizontal and vertical)
- Plate location (plate_x, plate_z)
- Spin axis
- Pitcher handedness (normalized so all pitchers share the same frame of reference)
- Batter handedness
- Count (balls and strikes)

**Model Architecture**

A separate XGBoost gradient boosting model was trained for each of the 13 pitch types. Training separate models per pitch type ensures the model learns what makes a fastball good independently of what makes a curveball good, since the physical profiles are fundamentally different across pitch types.

Each model was trained on 80% of the available pitches for that pitch type, with 20% held out as a test set.

Hyperparameters used: n_estimators=300, max_depth=5, learning_rate=0.05.

**Target Variable**

The model predicts delta_run_expectancy (delta_run_exp in Statcast), which measures the change in run expectancy associated with each pitch. Negative values are favorable for the pitcher.

**Scaling**

Raw model predictions were converted to a 100 based index using z score normalization, applied separately per pitch type:

```
Stuff+ = 100 - ((predicted_rv - mean_rv) / std_rv) * 10
```

This centers the distribution at 100 for each pitch type, with every 10 points representing one standard deviation from average.

---

## Results

**Top Pitches in 2025 (min. 100 pitches)**

| Pitcher | Pitch | Stuff+ |
|---|---|---|
| Taylor, Grant | CU | 110.6 |
| Megill, Trevor | FF | 109.3 |
| Duran, Jhoan | FS | 108.4 |
| Williams, Devin | CH | 108.4 |
| Clase, Emmanuel | FC | 107.1 |

**Sample Arsenal Table: Tarik Skubal**

| Pitch | Stuff+ | Velo | Spin | H-Break | V-Break | Usage% |
|---|---|---|---|---|---|---|
| CH | 102.5 | 88.0 | 1837 | -1.2 | 0.5 | 31.4 |
| FF | 103.6 | 97.6 | 2354 | -0.3 | 1.4 | 29.3 |
| SI | 102.6 | 97.3 | 2251 | -1.1 | 1.1 | 23.9 |
| SL | 102.0 | 90.0 | 2233 | 0.3 | 0.4 | 12.5 |
| CU | 98.7 | 81.2 | 2504 | 0.4 | -0.4 | 2.8 |

---

## Limitations & Next Steps

The current model produces scores that are more compressed than public Stuff+ models like FanGraphs, with most pitches scoring between 95 and 115 rather than the wider 60 to 150 range seen publicly. After research and comparison, the gap is attributable to several missing features:

**Velocity differential:** FanGraphs Stuff+ incorporates how a secondary pitch's velocity compares to a pitcher's primary fastball. A changeup that is 12mph slower than the fastball grades differently than one that is only 6mph slower, even if the raw velocity is identical. This differential is one of the strongest predictors of secondary pitch quality and is not currently in this model.

**Axis differential:** The difference between expected movement from spin and actual observed movement captures the seam shifted wake phenomenon, which affects how a pitch behaves in flight. This is a proprietary feature used in advanced pitch models that is not directly available in raw Statcast data.

**Next steps for a v2 model would include:**

Engineering velocity differential features relative to each pitcher's primary fastball, exploring CSW rate (called strike plus whiff rate) as an alternative target variable, and adding spin efficiency metrics derived from spin rate and axis data.

---

## Tools & Libraries

| Tool | Purpose |
|---|---|
| Python | Core language |
| pybaseball | Statcast data pull |
| pandas | Data manipulation |
| numpy | Numerical operations |
| XGBoost | Gradient boosting model |
| scikit-learn | Train/test split and validation |
| matplotlib | Visualizations |
| seaborn | Chart styling |
| pickle | Model serialization |

---

## Project Structure

```
mlb-stuff-plus-model/
├── data/
│   ├── raw/               # Raw Statcast CSVs by season
│   └── processed/         # Cleaned and scored data
├── src/
│   ├── data_pull.py       # Pulls Statcast data via pybaseball
│   ├── cleaning.py        # Cleans data and engineers features
│   ├── model.py           # Trains XGBoost models per pitch type
│   ├── validate.py        # Generates Stuff+ scores
│   └── visualize.py       # Arsenal tables and pitch movement plots
├── models/
│   └── stuff_plus_models.pkl
├── outputs/
│   └── figures/
├── README.md
└── requirements.txt
```
