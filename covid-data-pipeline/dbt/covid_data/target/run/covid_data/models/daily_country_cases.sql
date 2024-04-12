
  
    

  create  table "public"."analytics"."daily_country_cases__dbt_tmp"
  
  
    as
  
  (
    -- Select the current date in a dbt SQL model
-- select current_date as current_date

with daily_country_cases as (
    SELECT
        DATE(last_update) AS last_update,
        country_region,
        SUM(confirmed) AS total_confirmed_cases,
        SUM(deaths) AS total_deaths,
        SUM(recovered) AS total_recovered,
        SUM(active) AS total_active,
        AVG(incident_rate) AS mean_incident_rate,
        AVG(case_fatality_ratio) AS mean_case_fatality_ratio 
    FROM
        "public"."covid"."daily_report"
    GROUP BY
        DATE(last_update),
        country_region
    ORDER BY
        country_region
)

SELECT * FROM daily_country_cases
  );
  