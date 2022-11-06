INDEX_COLUMN_NAME = 'Unnamed: 0'

def clean_data(df):
	df.columns = ['index' if x==INDEX_COLUMN_NAME else x for x in df.columns]
	df = df.set_index('index')
	df = df.applymap(lambda s: s.lower() if type(s) == str else s)
	df = df.drop_duplicates(keep='first')
	return df
	# TODO:blanks?