# REFed take-home assignment

***A quick note on git***

Upon reading the assignment, I saw the phrase "Your final submission should be a zipped file directory" and assumed the output should specifically not be a git repository. This was purely a reading error on my part and I regret the missed chance to show you the way I work. I'm happy to talk through my process and prefer using git on all projects I work on.

For some insight into how I usually use git, feel free to browse the commit history, project organization, and PRs on a personal project of mine, [emojiphone](https://github.com/bromeostasis/emojiphone).

## Start here: Project overview and how to run

### Solution approach

The solution to this problem primarily leverages the `pandas` library to handle the sanitzation, manipulation, and calculation of the given food waste data. We can use the powerful `pandas` library to load the csv data into `DataFrame`s. We can then do some sanitization (lowercasing all strings) and sanity checks (ensuring no docuplicates) before saving a copy of the data to the `clean_data/` directory.

Once the data is cleaned, we use `pandas` `DataFrame`s to do row-level calculations. We're able to do the math required to calculate `tons_never_harvested` just by using the builtin dictionary-style column syntax.

To aggregate the data for plotting, we rely on the `pandas` `groupby` function, which allows us to roll up the data based on `year` and `refed_food_category`. We can then `sum` this grouped data and feed it into `matplotlib` to show a simple visualization of how many tons of food are wasted each year and by each category!

Finally, we read in the updated data and repeat the previous steps! We remove duplicates from the combined dataset (see future enhancements section for more details) and use the generalized methods from the first two steps to create new datasets and figures with updated 2018 and 2019 data.

### What's included

The solution presented here is mainly run via `main.py`. This script runs all three portions of the assignment and outputs the necessary data and figures into their appropriate directories. All supplementary and utility code is placed in subdirectories in order to maintain code readability. They are present in the `sanitzation/`, `analysis/`, and `plotting/` "packages".

All of the rest of the directories present are for input or output. They are as follows:

* `raw_data`: The input data presented in the problem. This remains unchanged throughout the solution for idempotency's sake.
* `clean_data`: The cleaned data; without duplicates, with lowercase strings, and an easily identifiable `index` column
* `production_data`: Cleaned data plus all calculated fields. These are the datasets we run analysis on and create our plots from
* `figures`: All plots present

Any file with the `v2_` prefix includes the updated 2018 & 2019 data from `farm_update_part_3.csv`.

Finally, I did keep the Jupyter notebook I used in the directory. It's fairly messy and disorganized as it's mainly notes and experiments, but feel free to take a look if you'd like!

### How to run

*This project was built using python version `3.7.3`. Please use this version or similar to ensure best results. See future enahcements section below for more details.*

Generating the data and figures is as simple as running the base command:

```python
python3 main.py
```
As mentioned in the assignment, I included the final data and figures in the directory.

If you'd like to clear out all of the generated output, I've included is a convenience script: `reset.py`. This will clear out everything except the raw data and can be run like this:
```python
python3 reset.py
# Verify here that all output directories are empty
python3 main.py
```

## Looking forward: Part 4 and Future Enhancements
### Part 4: Scaling the analytics pipeline
Currently, the solution exists as a local directory on a computer. In order to make this a scalable solution that works for a broader team, bigger datasets, and actual users, several things would need to change. I'll outline them here in priority order:

**Storage**

While `python` and `pandas` are very powerful, we don't want to rely on them, especially as our datasets grow in size. For one thing, we waste a lot of time and resources loading the data locally up every time to do analysis. Additionally, querying data in sql (I prefer [PostgreSQL](https://www.postgresql.org/)) is going to be much more performant than in python. For these reasons, we should start out by storing all of the "production data" in a database instead of outputting into more `csv` files. From there, we can query the data much faster in order to do more calculations on or run visualizations.

We would also want to store the `tons_never_harvested_by_cause` data in a dedicated table so we can easily update these values and have changes propogate throughout our system without having to update our code.

**Hosting**

We also need these analyses to be more broadly accessible to other engineers, more robust analytics solutions, and end-users. In order to do that, we need to host several parts of the solution in a publicly accessible location.

We would likely want to create a frontend interface where anyone (or anyone with appropriate permissions) could upload their data. To start with, this could be a simple file upload interface, though it could certainly expanded to show a lot of validation or be integrated with the current insights to help ensure that whoever might be submitting the data knows what they're doing and that they're submitting it to the right place.

We would also want to host the visualizations on a frontend server. Visualizations aren't a specialty of mine, so I'm not sure which technology would be best to use here, but we would certainly want the outside world to be able to view all of our work in a dynamic fashion, not just send them a folder of `.png`s!

Finally, we would need to host the backend calculations somewhere to ensure availability and scalability. A [Flask](https://flask.palletsprojects.com/en/2.2.x/) server would do well to get things up and running, though as datasets become larger (and more frequently updated) and calculations become more intensive, we may want to consider expanding into a task-based system such as [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) for some of our analysis and calculation, to ensure the frontend visualizations aren't impacted by uploads and analysis.

**Validation**

The current solution does not do much in terms of validating the cleanliness and sanity of the data coming in. Ensuring fields are the correct types, values are within acceptable parameters, and that there are no outliers will ensure our calculations are functional and accurate.

**Data Access**

Given that "engineers will need to be able to acess this data", it would likely be worth it to implement some sort of data visualization tool. Depending on the SQL knowledge of those accessing the data, we could consider using something like [Tableau](https://www.tableau.com/), [Snowflake](https://www.snowflake.com/en/), or [PowerBI](https://powerbi.microsoft.com/en-us/).


### Future Enhancements

For the sake of time, I made several tradeoffs that I would fix down the road. I've listed them here in rough order of what priority I'd fix/address them in:

* **More efficient calculations.** As previously mentioned, loading all the data into memory and doing calculations via `pandas` is not the most time-efficient. I also re-load the same data from a csv multiple times. With more time, I'd likely jump straight to storing data in Postgres and doing a lot of the heavy lifting there.
* **More sophisticated duplication detection.** Upon reviewing the dataset, I noticed that when rows are duplicated, all rows are exactly the same, including what I've renamed as "index". A more sophisticated solution would likely only check a subset of the columns to distinguish between strict copies and potential updates (a new dataset with the same year/crop, but newer numbers for wasted food).
* **Blank data detection.** The dataset also did not appear to have any blank data, so I did not implement anything to handle this case, but this is surely we'd run into in ramping up the pipeline.
* **Adding virutalenv.** To ensure more consistent execution across different computers, I would use virtualenv.
* **Friendlier script execution.** For convenience, it'd be nice to have the script take more inputs or be a bit more interactive. We could control things like filenames, output directories, resetting data, and potentially choosing which portions of the assignment to run.
* I also left a few smaller TODOs in the codebase for smaller cleanup tasks

## Miscellaneous: assumptions and corrections

Finally, here are a few assumptions I made and corrections I noticed in the assignment:

* Floats in the initial dataset were all rounded to the tenths place, so I continued to round all figures to that place.
* No names were specified for the "cause" columns, so I just went with `tons_never_harvested_<cause>`.
* In Appendix 1: Calculations, there is a change in a field name from `yields_tons_per_acre` to `yield_tons_per_acre`.


