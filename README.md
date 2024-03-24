# COVID Data Pipeline

This repository contains an end-to-end data pipeline for processing Johns Hopkins University COVID-19 dataset. This pipeline has a backfill for the date range of January 2020 to March 2023.
It consists of three main components: data loader, transformer, and data exporter. 

The data loader block extracts CSV data from the GitHub repository, while the transformer handles tasks such as managing missing values,
addressing inconsistent columns, dropping duplicate rows, and resolving data type conflicts.
Finally, the data exporter inserts the processed data into a Postgres table.

Initially, I attempted to utilize dbt with Mage, but encountered difficulties configuring it. As a result, I opted to utilize Python blocks within
Mage to avoid wasting time. This project presented a challenge for me as I needed to quickly familiarize myself with the Mage platform due to my lack of prior experience with it.

## Built with

1. Docker
2. Mage.ai
3. Python
4. PostgreSQL



## Folder Structure
```
├── covid-data-pipeline -- files from Mage.ai
│   ├── ...
│   ├── data_exporters
│   │   └── export_to_postgres.py
│   ├── data_loaders
│   │   └── api_load_data.py
│   ├── ...
│   ├── transformers
│   │   └── transform_data.py
│   ├── ...
│   └── io_config.yaml -- configuration file
├── mage_data -- contains cache 
├── .env -- environment variables
├── .gitignore
├── changes_over_time.py -- code to demonstrate metric change over time (for question #2)
├── correlation.py -- code to get the correlation between columns (for question #3)
├── data_analysis.sql -- query to get common values in a column (for question #1)
├── docker-compose.yml -- Docker compose file for MySQL and Python containers
├── Dockerfile -- Docker configuration file 
├── README.md
└── requirements.txt -- Python requirements file
```

## Setup Instructions

1. Clone the repository:
```
git clone https://github.com/cmagarap/covid-data-pipeline.git
```

2. Build the Docker image:
```
docker-compose build
```

3. Start the Docker container:
```
docker-compose up
```

4. Visit [localhost:6789](http://localhost:6789) and navigate to the pipelines on the left sidebar.
5. Click on `etl_pipeline` from the list of pipelines available.
6. Go to the `backfills` in the left sidebar.
7. Click on each backfill to run them:
```
2020_data_backfill
2021_data_backfill
2022_data_backfill
2023_data_backfill
```
8. Once finished, the data will be successfully loaded into the PostgreSQL database inside the Docker container.


## Additional Setup Notes
- Ensure that Docker is installed and running on your system before following these instructions.
- Make sure that a `.env` file exists inside the root directory with the necessary environment variables.
- Adjust any configuration settings as needed based on your environment.
- For further assistance or troubleshooting, refer to the documentation or open an issue in the repository.


# Data Analysis
1. What are the top 5 most common values in a particular column, and what is their frequency?

For country/region, the top 5 most common values are:
```
+-----------------+-----------+
| country_region  | frequency |
+-----------------+-----------+
| US              |   3514067 |
| Russia          |     84117 |
| Japan           |     49860 |
| China           |     37245 |
| India           |     37195 |
+-----------------+-----------+
SELECT country_region, COUNT(*) AS frequency
FROM covid.daily_reports
GROUP BY country_region
ORDER BY frequency DESC
LIMIT 5;
```
To find out other common values in a column, we can just change the `country_region` to other columns, for example:
```
SELECT province_state, COUNT(*) AS frequency
FROM covid.daily_reports
GROUP BY province_state
ORDER BY frequency DESC
LIMIT 5;

Result:
+-----------------+----------+
| province_state  | frequency|
+-----------------+----------+
| Texas           | 272341   |
| Georgia         | 174190   |
| Virginia        | 144970   |
| Kentucky        | 130145   |
| Missouri        | 125291   |
+-----------------+----------+
```

2. How does a particular metric change over time within the dataset?

As an example, I created a line graph to visualize the trend of confirmed Covid-19 cases:
![Cumulative Daily Confirmed COVID-19 cases in Los Angeles, California US](https://raw.githubusercontent.com/cmagarap/covid-data-pipeline/main/figures/covid19-CONFIRMED-Los-Angeles_California_US.png)
This line graph shows the increasing trend in the number of confirmed cases over time. At first, there appears to be a gradual rise in confirmed cases. However, over time, there are intervals when the rate of increase speeds up,
resulting in larger daily jumps in confirmed cases. The last entry in the data on March 10, 2023, reveals a considerable cumulative count of confirmed cases, indicating a noteworthy impact of COVID-19 throughout the duration encompassed by the dataset.
You may try to generate a difference graph using different metrics using the `changes_over_time.py` file.

3. Is there a correlation between two specific columns? Explain your findings.

To get the correlation between columns, I used Spearman correlation coefficient. (See `correlation.py`)
```
column1 = 'confirmed'
column2 = 'deaths'

# Calculate Spearman correlation coefficient
spearman_corr = df[[column1, column2]].corr(method='spearman').iloc[0, 1]
print(f"Spearman correlation coefficient between {column1} and {column2}: {spearman_corr}")
```

Output:
```
Spearman correlation coefficient between confirmed and deaths: 0.9212847975901324
```
1. The highest correlation is Confirmed and Deaths (0.921). The positive correlation coefficient of +0.921 suggests a direct relationship between confirmed cases and deaths. This means that as the number of confirmed cases rises, there is a corresponding increase in the number of deaths. This observation is consistent with our common understanding and the typical pattern seen during the COVID-19 pandemic, where higher confirmed case counts frequently coincide with higher fatality rates.
2. The second-highest correlation is Confirmed and Active cases (0.916). This could mean that when more cases are confirmed, it is likely that more individuals are actively infected and undergoing treatment or isolation.
3. The least correlation is Confirmed and Case Fatality Ratio (-0.032). The negative sign indicates the inverse relationship between the two columns. Since the correlation is close to zero, there is a little or no relationship between the two. Hence, fluctuations in confirmed cases do not significantly forecast case fatality ratio.

Additional note: When I used histogram on the data, I found out that they are not normally distributed. This has led me to use Spearman correlation because Pearson is used when the data follow a normal distribution.


