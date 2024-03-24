-- What are the top 5 most common values in a particular column, and what is their frequency?
SELECT country_region, COUNT(*) AS frequency
FROM covid.daily_reports
GROUP BY country_region
ORDER BY frequency DESC
LIMIT 5;