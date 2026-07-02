import pandas as pd
import numpy as np
import os

df1 = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2022.csv")
df2 = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2023.csv")
df3 = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2024.csv")
df_train = pd.concat([df1, df2, df3]).reset_index(drop=True)
df_2025 = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2025.csv")

column_list = ["player_name","pitch_type","release_speed","release_spin_rate","pfx_x","pfx_z",
               "release_extension","release_pos_x","release_pos_z","plate_x","plate_z","p_throws",
                "delta_run_exp","stand","balls","strikes","spin_axis"]

def clean_data(df):
    df_filtered = df[df['pitch_type'].notna()]
    df_filtered = df_filtered.dropna(subset = column_list)
    # print(df_filtered.shape)
    df_model = df_filtered[column_list].copy()
    # print("Before normalization:")
    # print(df_model.groupby('p_throws')['pfx_x'].mean())
    df_model['pfx_x'] = np.where(df_model['p_throws'] == 'L', -df_model['pfx_x'], df_model['pfx_x'])
    df_model['release_pos_x'] = np.where(df_model['p_throws'] == 'L', -df_model['release_pos_x'], df_model['release_pos_x'])
    df_model['stand'] = df_model['stand'].map({'R': 1, 'L': 0})
    # print(df_model.shape)
    # print(df_model.head(5))
    # print("After normalization:")
    # print(df_model.groupby('p_throws')['pfx_x'].mean())
    return df_model

df_train_clean = clean_data(df_train)
df_2025_clean = clean_data(df_2025)

print("Training data:", df_train_clean.shape)
print("2025 data:", df_2025_clean.shape)

df_train_clean.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\processed\pitches_train.csv")
df_2025_clean.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\processed\pitches_2025.csv")
