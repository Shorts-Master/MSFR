import pandas as pd

df = pd.read_csv('msfr_precursor_recirc_out_line_sample_0001.csv')
lambdas = [0.0126, 0.0337, 0.139, 0.325, 1.13, 2.50]
phi_peak_x = df.loc[df['phi'].idxmax(), 'x']

print(f"phi peak at x = {phi_peak_x}")
print(f"phi(0)={df['phi'].iloc[0]:.4f}  phi(224)={df['phi'].iloc[-1]:.4f}")
print()

for i, lam in enumerate(lambdas):
    col = f'C{i}'
    c0 = df[col].iloc[0]
    c_end = df[col].iloc[-1]
    peak_x = df.loc[df[col].idxmax(), 'x']
    offset = peak_x - phi_peak_x
    print(f"Group {i}: lambda={lam:>6}  C(0)={c0:.6e}  C(224)={c_end:.6e}  peak_x={peak_x:>5.0f}  offset={offset:>6.0f}")
