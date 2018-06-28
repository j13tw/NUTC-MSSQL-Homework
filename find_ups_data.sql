SELECT ups_status_in.uid, ups_status_in.iTime, iFreq, iLine, iVolt, oFreq, oLine, oMode, oAmp, oVolt, oWatt, oLoad, bStatus, bMode, bHealth, bLevel, bChangeDate, bReplaceDate, bVolt, bTemp, uIP, uName, uDistance, uNumber FROM ups_in as ups_status_in
INNER JOIN ups_battery on ups_status_in.uId = ups_battery.uId and ups_battery.bTime = ups_status_in.iTime
INNER JOIN ups_out on ups_status_in.uId = ups_out.uId and ups_status_in.iTime = ups_out.oTime
INNER JOIN ups on ups_status_in.uId = ups.uId
WHERE ups_status_in.iTime  >= '2018-06-28 18:00:30.000'and ups_status_in.iTime  <= '2018-06-28 18:01:30.000' and ups_status_in.uId = 'U001'
ORDER BY ups_status_in.iTime DESC
