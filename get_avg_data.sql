SELECT uId, AVG(iFreq) AS avg_iFreq, AVG(iVolt) AS avg_iVolt, iLine FROM ups_in 
WHERE DATENAME(second, iTime) = 07 and DATENAME(WEEKDAY, iTime) = '¬P´Á¤­'
GROUP BY uId, iLine
