SELECT tb1.Score AS Score, (SELECT COUNT(DISTINCT tb2.Score)
                            FROM tbl_scoreboard AS tb2
                            WHERE tb2.Score > tb1.Score)+1 AS Rank
FROM tbl_scoreboard AS tb1
ORDER BY tb1.Score DESC