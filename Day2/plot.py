import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('CompleteDataSet (2).csv', low_memory=False)
# keep original df for reference, make a numeric-converted copy for plotting
print('Initial shape:', df.shape)
print('Columns preview:', list(df.columns)[:10])

# Convert columns to numeric where possible (coerce errors to NaN)
df_numeric = df.apply(lambda col: pd.to_numeric(col, errors='coerce'))

# List detected numeric columns
numeric_cols = [c for c in df_numeric.columns if df_numeric[c].notna().sum() > 0]
print('Detected numeric columns (sample):', numeric_cols[:20])

# Use a cleaned numeric dataframe for plotting (do not drop all rows globally)


# Create histogram for Activity column
plt.figure(figsize=(10, 6))
df['Activity'].hist(bins=30, edgecolor='black', color='skyblue')
plt.title('Histogram of Activity')
plt.xlabel('Activity')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Alternative: Histogram for Subject using Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Subject', bins=15, kde=True, edgecolor='black')
plt.title('Histogram of Subject')
plt.xlabel('Subject')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# ---------------- Regression plot (explicit selection) ----------------
# You can specify columns by name: set `x_col_name` or `y_col_name`.
# Or specify by 1-based numeric index within detected numeric columns: set `x_index` / `y_index`.
# To use numeric column 2 as requested, set `x_index = 2` below.

# User override: set either of these variables (leave as None to use index selection)
x_col_name = None
y_col_name = None

# 1-based indices into `numeric_cols` (set x_index=2 to use numeric column 2)
x_index = 2
y_index = 3

# Determine x_col and y_col
if x_col_name is not None:
	x_col = x_col_name
elif len(numeric_cols) >= x_index:
	x_col = numeric_cols[x_index - 1]
else:
	x_col = None

if y_col_name is not None:
	y_col = y_col_name
elif len(numeric_cols) >= y_index:
	y_col = numeric_cols[y_index - 1]
else:
	y_col = None

if x_col is None or y_col is None:
	print('Cannot determine x_col/y_col for regression. Check `numeric_cols` and indices.')
	print('Detected numeric columns (first 20):', numeric_cols[:20])
else:
	print(f'Using columns for regression: x={x_col}, y={y_col}')
	reg_df = df_numeric[[x_col, y_col]].dropna()
	if reg_df.empty:
		print('No valid numeric pairs found for regression after dropping NA.')
	else:
		plt.figure(figsize=(8, 6))
		sns.regplot(x=reg_df[x_col], y=reg_df[y_col], scatter_kws={'s': 10, 'alpha': 0.5}, line_kws={'color': 'red'})
		plt.title(f'Regression: {y_col} vs {x_col}')
		plt.xlabel(x_col)
		plt.ylabel(y_col)
		plt.tight_layout()
		plt.show()
