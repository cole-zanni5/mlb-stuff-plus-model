import pandas as pd
import numpy as np
import os
import xgboost as xgb
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

df = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\processed\pitches_train.csv")

feature_cols = ["release_speed","release_spin_rate","pfx_x","pfx_z",
                "release_extension","release_pos_x","release_pos_z",
                "plate_x","plate_z","stand","balls","strikes","spin_axis"]
target_col = "delta_run_exp"

pitch_types = df['pitch_type'].unique()
print(pitch_types)
df = df[~df['pitch_type'].isin(["PO","UN","EP","SC","FA"])]
pitch_types = df['pitch_type'].unique()
print(pitch_types)

models = {}

for pt in pitch_types:
    df_pt = df[df["pitch_type"] == pt]
    X = df_pt[feature_cols]
    y = df_pt[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                        random_state=42)
    model = xgb.XGBRegressor(n_estimators=300, max_depth=5,
                             learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    models[pt] = model
    print(pt," DONE")

with open(r'C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\models\stuff_plus_models.pkl', 'wb') as f:
    pickle.dump(models, f)

with open(r'C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\models\stuff_plus_models.pkl', 'rb') as f:
    loaded_models = pickle.load(f)

print(loaded_models.keys())
