import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# FF - Four-seam fastball
# SI - Sinker
# FC - Cutter
# FS - Splitter
# SL - Slider
# ST - Sweeper
# CU - Curveball
# KC - Knuckle curve
# CS - Slow curve
# CH - Changeup
# SV - Slurve
# KN - Knuckleball
# FO - Forkball

df = pd.read_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\processed\pitches_scored.csv")
OUTPUT_DIR = r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\outputs\figures"

leaderboard = df.groupby(['player_name','pitch_type'])['stuff_plus'].agg(['mean','count']).reset_index()
leaderboard = leaderboard[leaderboard['count'] > 100 ] 
leaderboard = leaderboard.rename(columns={'mean':'stuff_plus'})
leaderboard = leaderboard.sort_values('stuff_plus',ascending=False)
top20 = leaderboard.head(20)

vertical = 'pfx_z'
horizontal = 'pfx_x'


def plot_pitch_landscape(pitcher_name, pitch_type_code, movement, show=True):
    df_pitch = df[df['pitch_type'] == pitch_type_code]
    df_pitcher = df[(df['pitch_type'] == pitch_type_code) & (df['player_name'] == pitcher_name)]
    x = df_pitch['release_speed']
    y = df_pitch[movement]
    color = df_pitch['stuff_plus']

    fig = plt.figure(figsize=(10, 8))
    plt.hexbin(x, y, C=color, gridsize=20, cmap='RdYlBu_r', reduce_C_function=np.mean,
               vmin=85, vmax=115)
    plt.colorbar(label='Stuff+')
    if movement == 'pfx_z':
        plt.ylabel('vertical movement')
        move_label = 'Vertical'
    else:
        plt.ylabel('horizontal movement')
        move_label = 'Horizontal'
    plt.title(pitcher_name + ' 2025 ' + pitch_type_code + ' ' + move_label + ' Stuff+ Landscape')
    plt.xlabel('velocity')
    plt.scatter(df_pitcher['release_speed'].mean(),
                df_pitcher[movement].mean(),
                color='black', s=200, zorder=5, label=pitcher_name + ' ' + pitch_type_code
                )
    plt.axvline(x=df_pitcher['release_speed'].mean(), color='black')
    plt.axhline(y=df_pitcher[movement].mean(), color='black')
    plt.legend()

    if show:
        plt.show()

    return fig


def arsenal_table(pitcher_name):
    df_pitcher = df[df['player_name'] == pitcher_name]
    means = df_pitcher.groupby('pitch_type')[['stuff_plus', 'release_speed', 'release_spin_rate', 'pfx_x', 'pfx_z']].mean()
    counts = df_pitcher.groupby('pitch_type')['pitch_type'].count()
    means['count'] = counts
    means['usage'] = (means['count'] / len(df_pitcher)) * 100
    means = means.rename(columns={
        'stuff_plus': 'Stuff+',
        'release_speed': 'Velo',
        'release_spin_rate': 'Spin',
        'pfx_x': 'H-Break',
        'pfx_z': 'V-Break',
        'usage': 'Usage%'
    }).sort_values('Usage%', ascending=False).drop(columns=['count'])
    means = means.round(1)
    means = means[means['Usage%'] > 1]
    return means


def movement_plot(pitcher_name, show=True):
    df_pitcher = df[df['player_name'] == pitcher_name]
    fig = plt.figure(figsize=(10, 8))
    plt.title(pitcher_name + ' 2025 Pitch Movement')
    plt.xlabel('Horizontal Break (in)')
    plt.ylabel('Vertical Break (in)')
    for pt in df_pitcher['pitch_type'].unique():
        df_pt = df_pitcher[df_pitcher['pitch_type'] == pt]
        sc = plt.scatter(df_pt['pfx_x'], df_pt['pfx_z'], label=pt, alpha=0.4, s=10)
        plt.scatter(df_pt['pfx_x'].mean(), df_pt['pfx_z'].mean(), color=sc.get_facecolor()[0],
                    s=150, edgecolors='black', linewidths=1.5)
    for handle in plt.legend().legend_handles:
        handle.set_sizes([50])
    plt.axvline(x=0, color='black')
    plt.axhline(y=0, color='black')
    plt.legend()
    plt.xlim(-2.0, 2.0)
    plt.ylim(-2.0, 2.0)

    if show:
        plt.show()

    return fig


def save_plots(pitcher_name, output_dir, pitch_types=None):
    # --- MOVEMENT ---
    fig = movement_plot(pitcher_name, show=False)
    fig.savefig(output_dir + fr"\{pitcher_name}_movement.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    # --- if not provided, default to all ---
    if pitch_types is None:
        df_pitcher = df[df['player_name'] == pitcher_name]
        pitch_types = df_pitcher['pitch_type'].unique()
    elif isinstance(pitch_types, str):
        pitch_types = [pitch_types]

    # --- LANDSCAPE ---
    for pt in pitch_types:
        for movement in ['pfx_z', 'pfx_x']:
            fig = plot_pitch_landscape(pitcher_name, pt, movement, show=False)
            move_label = "vertical" if movement == "pfx_z" else "horizontal"
            fig.savefig(
                output_dir + fr"\{pitcher_name}_{pt}_{move_label}_landscape.png",
                dpi=150,
                bbox_inches="tight"
            )
            plt.show()
            plt.close(fig)


pitcher = 'Clase, Emmanuel'
pitchType = 'FC'
save_plots(pitcher, OUTPUT_DIR, pitchType)