import pandas as pd
import numpy as np
import pickle

df = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\processed\pitches_2025.csv")
with open(r'C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\models\stuff_plus_models.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

df = df[~df['pitch_type'].isin(["PO","UN","EP","SC","FA"])]
pitch_types = df['pitch_type'].unique()
df['predicted_rv'] = 0.0
feature_cols = ["release_speed","release_spin_rate","pfx_x","pfx_z",
                "release_extension","release_pos_x","release_pos_z",
                "plate_x","plate_z","stand","balls","strikes","spin_axis"]

for pt in pitch_types:
    df_pt = df[df["pitch_type"] == pt]
    X = df_pt[feature_cols]
    predictions = loaded_model[pt].predict(X)
    df.loc[df['pitch_type'] == pt, 'predicted_rv'] = predictions

df["stuff_plus"] = 0.0

for pt in pitch_types:
    df_pt = df[df["pitch_type"] == pt]
    mean_rv = df_pt["predicted_rv"].mean()
    std_rv = df_pt["predicted_rv"].std()
    df.loc[df["pitch_type"] == pt, 'stuff_plus'] = 100 - ((df_pt["predicted_rv"] - mean_rv) / std_rv) * 15

# print(df[['player_name', 'pitch_type', 'predicted_rv', 'stuff_plus']].head(10))


leaderboard = df.groupby(['player_name','pitch_type'])['stuff_plus'].agg(['mean','count']).reset_index()
leaderboard = leaderboard[leaderboard['count'] > 100 ] 
leaderboard = leaderboard.rename(columns={'mean':'stuff_plus'})
leaderboard = leaderboard.sort_values('stuff_plus',ascending=False)
print(leaderboard.head(20))

df.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\processed\pitches_scored.csv")
