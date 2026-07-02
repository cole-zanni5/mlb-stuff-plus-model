import pandas as pd
import pybaseball as pyb
import os

pyb.cache.enable()
# start_dt = "2022-03-27"
# end_dt = "2022-09-28"
# df = pyb.statcast(start_dt, end_dt)
# df.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2022.csv")

# start_dt = "2023-03-27"
# end_dt = "2023-09-28"
# df = pyb.statcast(start_dt, end_dt)
# df.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2023.csv")

start_dt = "2024-03-27"
end_dt = "2024-09-28"
df = pyb.statcast(start_dt, end_dt)
df.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2024.csv")

# start_dt = "2025-03-27"
# end_dt = "2025-09-28"
# df = pyb.statcast(start_dt, end_dt)
# df.to_csv(r"C:\Users\colez\Documents\GitHub\mlb-stuff-plus-model\data\raw\statcast_2025.csv")

# print(df.shape)
# print(df.head(5))
# print(df.columns.tolist())
# print(df[['release_speed', 'release_spin_rate', 'pfx_x', 'pfx_z', 
#           'release_extension', 'delta_run_exp']].isnull().sum())