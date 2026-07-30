import pandas as pd

df = pd.read_csv("sweep_6group_summary.csv")

L_half = df['phi_peak_x'].iloc[-1]  # domain half-length (flux peak location), same across all rows
print(f"L_half = {L_half:.1f} cm\n")

rows = []
for i in range(6):
    lam = df[f'lambda_{i}'].iloc[0]
    for _, row in df.iterrows():
        v = row['velocity']
        offset = row[f'offset_{i}']
        if v == 0:
            continue
        x = v / (lam * L_half)          # dimensionless drift number
        y = offset / L_half              # normalized offset
        rows.append({'group': i, 'lambda': lam, 'velocity': v, 'x_dimensionless': x, 'y_normalized': y})

collapse_df = pd.DataFrame(rows)
collapse_df.to_csv("collapse_check.csv", index=False)

print(collapse_df.sort_values('x_dimensionless').to_string(index=False))
