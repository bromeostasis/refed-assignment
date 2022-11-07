#!/usr/bin/env python3

import pandas as pd
import csv

from sanitization.sanitize import clean_data
from analysis.calculations import *
from plotting.plot import *

# Constants / shared variables

part_1_csv_filename = 'raw_data/farm_part_1.csv'
part_3_csv_filename = 'raw_data/farm_update_part_3.csv'
not_harvested_csv_filename = 'raw_data/farm_not_harvested_causes.csv'

part_1_prod_filename = 'prod_data/farm_part_1_production.csv'

df_harvest = pd.read_csv(not_harvested_csv_filename)

def main():
	assignment_part_1()
	assignment_part_2()
	assignment_part_3()

def assignment_part_1():
	df_1 = pd.read_csv(part_1_csv_filename)

	df_1 = clean_data(df_1)
	df_1.to_csv('clean_data/farm_part_1_clean.csv')
	df_1 = calculate_tons_never_harvested(df_1)
	df_1 = calculate_tons_never_harvested_by_cause(df_1, df_harvest)
	df_1.to_csv(part_1_prod_filename)

def assignment_part_2():
	df_2 = pd.read_csv(part_1_prod_filename) # Note: Choosing to not use a shared data frame to emulate an importing of productin data

	plot_not_harvested_by_year(df_2, 'not_harvested_by_year')
	plot_not_harvested_by_year_and_dept(df_2, 'not_harvested_by_year_and_dept')
	plot_not_harvested_by_cause(df_2, df_harvest, 'not_harvested_by_cause')

def assignment_part_3():
	df_3 = pd.read_csv(part_3_csv_filename)

	df_3 = clean_data(df_3)
	df_3.to_csv('clean_data/farm_part_3_clean.csv')
	df_3 = calculate_tons_never_harvested(df_3)
	df_3 = calculate_tons_never_harvested_by_cause(df_3, df_harvest)
	
	df_2 = pd.read_csv(part_1_prod_filename, index_col='index') # Note: Choosing to not use a shared data frame to emulate an importing of productin data
	df_final = df_2.append(df_3)
	df_final = df_final.drop_duplicates(keep='first')
	df_final.to_csv('prod_data/v2_farm_production.csv')

	plot_not_harvested_by_year(df_final, 'v2_not_harvested_by_year')
	plot_not_harvested_by_year_and_dept(df_final, 'v2_not_harvested_by_year_and_dept')
	plot_not_harvested_by_cause(df_final, df_harvest, 'v2_not_harvested_by_cause')

main()
