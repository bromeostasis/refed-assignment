import matplotlib.pyplot as plt

def autopct_format(values):
    def actual_value(pct):
        total = sum(values)
        val = round(pct*total/100.0, 1)
        return str(val)
    return actual_value

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
	labels = [f'{str(year_and_dept[0])} ({year_and_dept[1]})' for year_and_dept in data_by_year_and_dept.indices.keys()]

	plt.pie(plot_data, labels=labels, autopct=autopct_format(plot_data))
	plt.title('Tons never harvested by year and department')
	plt.savefig(f'figures/{plot_name}.png')

def plot_not_harvested_by_cause(df, df_harvest, plot_name):
	data_by_year_and_dept = df.groupby(['year', 'refed_food_department']) # TODO: repeated group by..

	for index, row in df_harvest.iterrows():
		plt.clf()

		plot_data = data_by_year_and_dept.sum()[f'tons_never_harvested_{row.cause}']
		labels = [f'{str(year_and_dept[0])} ({year_and_dept[1]})' for year_and_dept in data_by_year_and_dept.indices.keys()]

		plt.pie(plot_data, labels=labels, autopct=autopct_format(plot_data))
		display_name = row.cause.replace('_', ' ')
		plt.title(f'Tons never harvested by year and department for cause "{display_name}"')
		plt.savefig(f'figures/{plot_name}_{row.cause}.png')
