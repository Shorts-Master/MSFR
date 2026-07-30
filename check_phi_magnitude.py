import pandas as pd

df = pd.read_csv('msfr_precursor_recirc_out_line_sample_0001.csv')
print(f"phi max value  = {df['phi'].max():.6e}")
print(f"phi min value  = {df['phi'].min():.6e}")
print()
print(df[['x','phi']].iloc[::20].to_string(index=False))
