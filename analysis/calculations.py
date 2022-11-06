def calculate_tons_never_harvested(df):
	df['acres_unharvested'] = df['acres_planted']  - df['acres_harvested']
	df['yield_tons_per_acre'] = round(df['tons_harvested'] / df['acres_harvested'], 1) # Division!??!
	df['price_per_ton'] = round(df['us_dollars_harvested'] / df['tons_harvested'], 1)
	df['tons_never_harvested'] = round(df['acres_unharvested'] * df['yield_tons_per_acre'] * df['percent_maturity'], 1)
	return df

def calculate_tons_never_harvested_by_cause(df, df_harvest):
	for index, row in df_harvest.iterrows():
	    df[f'tons_never_harvested_{row.cause}'] = round(df['tons_never_harvested'] * row.rate, 1)
	return df
