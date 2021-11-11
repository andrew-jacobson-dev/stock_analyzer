SELECT *
  FROM
       (SELECT id, --[0]
               stock_id, --[1]
               d_process, --[2]
               a_close_delta as "a_one_day_close", --[3]
               lag(a_close_delta, 1) over (order by d_process) as "a_2_day_close", --[4]
               lag(a_close_delta, 2) over (order by d_process) as "a_3_day_close", --[5]
               lag(a_close_delta, 3) over (order by d_process) as "a_4_day_close", --[6]
               lag(a_close_delta, 4) over (order by d_process) as "a_5_day_close", --[7]
               lag(a_close_delta, 5) over (order by d_process) as "a_6_day_close", --[8]
               lag(a_close_delta, 6) over (order by d_process) as "a_7_day_close", --[9]
               lag(a_close_delta, 7) over (order by d_process) as "a_8_day_close", --[10]
               lag(a_close_delta, 8) over (order by d_process) as "a_9_day_close", --[11]
               lag(a_close_delta, 9) over (order by d_process) as "a_9_day_close", --[12]
               lag(a_close_delta, 10) over (order by d_process) as "a_10_day_close", --[13]
               lag(a_close_delta, 11) over (order by d_process) as "a_11_day_close", --[14]
               lag(a_close_delta, 12) over (order by d_process) as "a_12_day_close", --[15]
               lag(a_close_delta, 13) over (order by d_process) as "a_13_day_close", --[16]
               lag(a_close_delta, 14) over (order by d_process) as "a_14_day_close", --[17]
               a_close, --[18]
               a_previous_close, --[19]
               a_avg_volume, --[20]
               a_volume, --[21]
               lag(a_volume, 1) over (order by d_process) as "a_2_day_volume", --[22]
               lag(a_volume, 2) over (order by d_process) as "a_3_day_volume", --[23]
               lag(a_volume, 3) over (order by d_process) as "a_4_day_volume", --[24]
               lag(a_volume, 4) over (order by d_process) as "a_5_day_volume", --[25]
               lag(a_volume, 5) over (order by d_process) as "a_6_day_volume", --[26]
               lag(a_volume, 6) over (order by d_process) as "a_7_day_volume", --[27]
               a_fifty_two_week_high, --[28]
               a_fifty_two_week_low, --[29]
               a_forward_eps, --[30]
               a_trailing_eps --[31]
          FROM stock_summary_stockeod
         WHERE stock_id = %s
      ORDER BY D_PROCESS DESC
         ) stock_summary_stockeod
LIMIT 1;