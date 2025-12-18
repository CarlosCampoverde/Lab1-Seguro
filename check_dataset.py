import pandas as pd

df = pd.read_json('diversevul.json', lines=True)
print(f"Total ejemplos: {len(df)}")
print(f"Vulnerables (target=1): {(df['target']==1).sum()}")
print(f"Seguros (target=0): {(df['target']==0).sum()}")
print(f"\nBalance: {((df['target']==1).sum() / len(df) * 100):.1f}% vulnerables")
