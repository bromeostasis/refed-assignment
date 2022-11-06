import matplotlib.pyplot as plt

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return str(val)
    return my_format

def plot_not_harvested_by_year(df, plot_name):
	plt.clf()
	data_by_year = df.groupby(['year'])
	plot_data = data_by_year.sum().tons_never_harvested

	plt.pie(plot_data, labels=data_by_year.indices.keys(), autopct=autopct_format(plot_data))
	plt.title('Tons never harvested by year')
	plt.savefig(f'figures/{plot_name}.png') # TODO: Not relative path? Path safety?

def plot_not_harvested_by_year_and_dept(df, plot_name):
	plt.clf()
	data_by_year_and_dept = df.groupby(['year', 'refed_food_department'])
	plot_data = data_by_year_and_dept.sum().tons_never_harvested
	labels = data_by_year_and_dept.indices.keys()
	labels = [f'{str(tuple[0])} ({tuple[1]})' for tuple in labels]

	plt.pie(plot_data, labels=labels, autopct=autopct_format(plot_data))
	plt.title('Tons never harvested by year and refed department')
	plt.savefig(f'figures/{plot_name}.png')

def plot_not_harvested_by_cause(df, df_harvest, plot_name):
	data_by_year_and_dept = df.groupby(['year', 'refed_food_department']) # TODO: repeated group by..

	for index, row in df_harvest.iterrows():
		plt.clf()
		
		labels = data_by_year_and_dept.indices.keys()
		labels = [f'{str(tuple[0])} ({tuple[1]})' for tuple in labels]
		plot_data = data_by_year_and_dept.sum()[f'tons_never_harvested_{row.cause}']

		plt.pie(plot_data, labels=labels, autopct=autopct_format(plot_data))
		display_name = row.cause.replace('_', ' ')
		plt.title(f'Tons never harvested for {display_name}')
		plt.savefig(f'figures/{plot_name}_{row.cause}.png')
