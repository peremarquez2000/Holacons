SELECT NPassengers,
	   OpCo,
	   ArrivalAirport as Country,
	   ArrivalAirport as Region,
	   strftime('%Y', Date) AS Year,
       CASE
           WHEN strftime('%m', Date) BETWEEN '01' AND '03' THEN 'Q1'
           WHEN strftime('%m', Date) BETWEEN '04' AND '06' THEN 'Q2'
           WHEN strftime('%m', Date) BETWEEN '07' AND '09' THEN 'Q3'
           WHEN strftime('%m', Date) BETWEEN '10' AND '12' THEN 'Q4'
       END AS Quarter
FROM Flights 
GROUP BY OpCo, Country, Region, Year, Quarter