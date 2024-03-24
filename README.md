# COVID Data Pipeline

This repository contains an end-to-end data pipeline for processing Johns Hopkins University COVID-19 dataset.

## Built with

1. Docker
2. Mage.ai
3. Python
4. 
TODO: [A brief explanation of your design decisions and the technologies used.]

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
├── changes_over_time.py -- Python code to demonstrate metric change over time
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
7. Click on each backfill to run them.
8. Once finished, the data will be successfully loaded into the PostgreSQL database inside the Docker container.


## Additional Setup Notes
- Ensure that Docker is installed and running on your system before following these instructions.
- Make sure that a `.env` file exists inside the root directory with the necessary environment variables.
- Adjust any configuration settings as needed based on your environment.
- For further assistance or troubleshooting, refer to the documentation or open an issue in the repository.


## Data Analysis
1. What are the top 5 most common values in a particular column, and what is their frequency?
2. How does a particular metric change over time within the dataset?

As an example, I created a line graph to visualize the trend of confirmed Covid-19 cases:
[Cumulative Daily Confirmed COVID-19 cases in Los Angeles, California US]('https://raw.githubusercontent.com/cmagarap/covid-data-pipeline/main/figures/covid19-CONFIRMED-Los-Angeles_California_US.png)

3. Is there a correlation between two specific columns? Explain your findings.
