SELECT tub_asia.tub, asia, SUM(tub_asia.prob*asia.prob) 
FROM (
	SELECT asia.asia as asia 
	FROM asia
	GROUP BY asia
	)
INNER JOIN tub_asia 
ON asia=tub_asia.asia GROUP BY tub_asia.tub;
