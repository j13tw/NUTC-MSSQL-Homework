/****** SSMS 中 SelectTopNRows 命令的指令碼  ******/
SELECT TOP (1000) [uId]
      ,[iFreq]
      ,[iVolt]
      ,[iLine]
      ,[iTime]
  FROM [1410432021].[dbo].[ups_in]
  where DATENAME(second, iTime) = 07