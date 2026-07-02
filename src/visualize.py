import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

leaderboard = df.groupby(['player_name','pitch_type'])['stuff_plus'].agg(['mean','count']).reset_index()
leaderboard = leaderboard[leaderboard['count'] > 100 ] 
leaderboard = leaderboard.rename(columns={'mean':'stuff_plus'})
leaderboard = leaderboard.sort_values('stuff_plus',ascending=False)
top20 = leaderboard.head(20)
# print(leaderboard.sort_values('stuff_plus', ascending=True).head(20))
# print(top20)

vertical = 'pfx_z'
horizontal = 'pfx_x'

def plot_pitch_landscape(pitcher_name, pitch_type_code, movement):
    df_pitch = df[df['pitch_type'] == pitch_type_code]
    df_pitcher = df[(df['pitch_type'] == pitch_type_code) & (df['player_name'] == pitcher_name)]
    x = df_pitch['release_speed']
    y = df_pitch[movement]
    color = df_pitch['stuff_plus']
    plt.figure(figsize=(10,8))
    plt.hexbin(x, y, C=color, gridsize=20, cmap='RdYlBu_r', reduce_C_function=np.mean, 
               vmin=85, vmax=115)
    plt.colorbar(label='Stuff+')
    plt.title('2025 '+pitch_type_code+" Stuff+ Landscape")
    plt.xlabel('velocity')
    if movement == 'pfx_z':
        plt.ylabel('vertical movement')
    else:
        plt.ylabel('horizontal movement')
    plt.scatter(df_pitcher['release_speed'].mean(),
                df_pitcher[movement].mean(),
                color='black', s=200, zorder=5, label=pitcher_name+' '+pitch_type_code
                )
    plt.axvline(x=df_pitcher['release_speed'].mean(), color='black')
    plt.axhline(y=df_pitcher[movement].mean(), color='black')
    plt.legend()
    plt.show()

def arsenal_table(pitcher_name):
    df_pitcher = df[df['player_name'] == pitcher_name]
    means = df_pitcher.groupby('pitch_type')[['stuff_plus', 'release_speed', 'release_spin_rate', 'pfx_x', 'pfx_z']].mean()
    counts = df_pitcher.groupby('pitch_type')['pitch_type'].count()
    means['count'] = counts
    means['usage'] = (means['count'] / len(df_pitcher)) * 100
    means = means.rename(columns = {
    'stuff_plus': 'Stuff+',
    'release_speed': 'Velo',
    'release_spin_rate': 'Spin',
    'pfx_x': 'H-Break',
    'pfx_z': 'V-Break',
    'usage': 'Usage%'
    }).sort_values('Usage%',ascending=False).drop(columns=['count'])
    means = means.round(1)
    means = means[means['Usage%'] > 1]
    return means

def movement_plot(pitcher_name):
    df_pitcher = df[df['player_name'] == pitcher_name]
    plt.figure(figsize=(10,8))
    plt.title(pitcher_name+' 2025 Pitch Movement')
    plt.xlabel('Horizontal Break (in)')
    plt.ylabel('Vertical Break (in)')
    for pt in df_pitcher['pitch_type'].unique():
        df_pt = df_pitcher[df_pitcher['pitch_type'] == pt]
        sc = plt.scatter(df_pt['pfx_x'], df_pt['pfx_z'], label=pt, alpha=0.4, s=10)
        plt.scatter(df_pt['pfx_x'].mean(), df_pt['pfx_z'].mean(),color=sc.get_facecolor()[0], s=150, edgecolors='black', linewidths=1.5)
    for handle in plt.legend().legend_handles:
        handle.set_sizes([50])
    plt.axvline(x=0, color='black')
    plt.axhline(y=0, color='black')
    plt.legend()
    plt.xlim(-2.0, 2.0)
    plt.ylim(-2.0, 2.0)
    plt.show()




# plot_pitch_landscape('Duran, Jhoan', 'FS', vertical)
# plot_pitch_landscape('Duran, Jhoan', 'FS', horizontal)
# plot_pitch_landscape('Skubal, Tarik', 'CH', horizontal)
# plot_pitch_landscape('Skenes, Paul', 'FF', vertical)
# plot_pitch_landscape('Helsley, Ryan', 'FF', vertical)
# plot_pitch_landscape('Clase, Emmanuel', 'FC', vertical)
# plot_pitch_landscape('Crochet, Garrett', 'ST', horizontal)
# plot_pitch_landscape('Hendricks, Kyle', 'FF', vertical)
# plot_pitch_landscape('Senga, Kodai', 'SI', vertical)

# print(arsenal_table('Skubal, Tarik'))
# print(arsenal_table('Skenes, Paul'))
# print(arsenal_table('Clase, Emmanuel'))

print(movement_plot('Skubal, Tarik'))
print(movement_plot('Skenes, Paul'))