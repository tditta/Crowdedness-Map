import pandas as pd
import random
random.seed(1)

df = pd.read_csv("60615_locations.csv")

reliable_index = df.index[df.unreliable == 0]

levels = [0, 1, 2]
levels_vars = ["crowded_place", "crowded_grocery", "crowded_restaurant", "comp_to_grocery"]
for var in levels_vars:
    df.loc[reliable_index, var] = [random.choice(levels) for i in reliable_index]

h_range = range(1, 7) 
for h in h_range:
    hour_start = 8 + (h - 1) * 2
    hour_end = hour_start + 1
    hours = list(range(hour_start, hour_end + 1)) + [-1]
    if h == 1:
        df.loc[reliable_index, "hofd%i" % h] = [random.choice(hours) for i in reliable_index]
    else:
        has_prev_hour = df.index[df["hofd%i" % (h - 1)] >= 0]
        df.loc[has_prev_hour, "hofd%i" % h] = [random.choice(hours) for i in has_prev_hour]
for h in h_range:
    df.loc[df["hofd%i" % h] == -1, "hofd%i" % h] = None

d_range = range(1, 4)
for d in d_range:
    day_start = (d - 1) * 2
    day_end = day_start + 1
    days = list(range(day_start, day_end + 1)) + [-1]
    if d == 1:
        df.loc[reliable_index, "dofw%i" % d] = [random.choice(days) for i in reliable_index]
    else:
        has_prev_day = df.index[df["dofw%i" % (d - 1)] >= 0]
        df.loc[has_prev_day, "dofw%i" % d] = [random.choice(days) for i in has_prev_day]
for d in d_range:
    df.loc[df["dofw%i" % d] == -1, "dofw%i" % d] = None

df.to_csv("../fake_data.csv", index = False)
