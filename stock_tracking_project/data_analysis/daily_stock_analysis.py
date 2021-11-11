import psycopg2
import yfinance as yf
from datetime import datetime, timedelta

import os, sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from stocks_db_config import stocks_db_config
from stocks_email_config import stocks_email_config
from jobs.job_run import JobRun


def determine_status(insert_record):

    status = 'determining'

    # Evaluate the average volume - don't want anything less than 400000 (per expert advice)
    average_volume = insert_record[3]

    if average_volume < 400000:
        status = 'avg vol too low'
    else:
        # Evaluate consecutive number of days down/up
        days_down = insert_record[4]
        price_change = insert_record[5]
        percent_change = insert_record[6]

        # Stock is trending down
        if days_down > 2 and price_change < -10 and percent_change < -2:
            status = 'buy'
        # Stock is up
        elif days_down < -2 and price_change > 10:
            status = 'sell'
        else:
            status = 'hold'

    insert_record[2] = status

    return insert_record


# ~~~~~~~~ Main program ~~~~~~~~ #
debug = False

# Open DB connection and create the cursor
db_connection = stocks_db_config.open_connection_to_db()
db_cursor = stocks_db_config.open_db_cursor(db_connection)

# Create JobRun object
new_job = JobRun('daily stock analysis', 'daily_stock_analysis.py', 'not run', 'not run')

# Calculate data date
data_date = datetime.now().date() - timedelta(1)

# Check date to see if the stock market was even open yesterday
db_cursor.execute("""SELECT 1 FROM data_pull_nyseholiday WHERE d_holiday = %s;""", (data_date,))

# Process as normal if it was not a holiday yesterday
if db_cursor.fetchone() is None:

    # Counter variables for processing
    total_stocks_count = 0
    insert_counter = 0
    error_count = 0

    # Store any stocks that had problems processing
    error_stocks = []

    # Execute Select statement to get the total number of stocks
    db_cursor.execute("SELECT count(*) FROM stock_summary_stock;")
    total_stocks_count = db_cursor.fetchone()[0]

    # Get the first query from the designated file
    fd = open('/home/ubuntu/stocks/data_analysis/stock_analysis_query1.sql', 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommand = sqlFile.split(';')
    sqlCommand = sqlCommand[0]

    # Execute Select statement to get the list of stocks
    db_cursor.execute("SELECT id, n_symbol FROM stock_summary_stock;")
    all_stocks = db_cursor.fetchall()

    for stock in all_stocks:

        try:
            # Execute the SQL query for the specified Stock id
            db_cursor.execute(sqlCommand, (stock[0],))

            # Get the row from the cursor
            stockEOD_row = db_cursor.fetchone()

            stockEODProfile_stockEOD = stockEOD_row[0]
            stockEODProfile_d_evaluation = data_date
            stockEODProfile_t_status = 'unknown'
            stockEODProfile_a_avg_volume = stockEOD_row[20]
            ############################################################################################################
            # Stock price trend analysis
            stockEODProfile_q_consecutive_days_down = 0
            stockEODProfile_a_consecutive_days_price_change = 0

            # Check the first close price value from the query: if it's negative, look for consecutive down days; if
            # it's positive, look for consecutive positive days
            if stockEOD_row[3] < 0:

                # Process the last 14 days of close prices
                for x in range(3, 18):

                    if stockEOD_row[x] < 0:
                        stockEODProfile_q_consecutive_days_down += 1
                        stockEODProfile_a_consecutive_days_price_change += stockEOD_row[x]
                    else:
                        break
            else:

                # Process the last 14 days of close prices
                for x in range(3, 18):

                    if stockEOD_row[x] > 0:
                        stockEODProfile_q_consecutive_days_down -= 1
                        stockEODProfile_a_consecutive_days_price_change += stockEOD_row[x]
                    else:
                        break

            # Calculate the price change percentage since the stock started going down or up
            current_stock_price = stockEOD_row[18]
            old_stock_price = 0

            # If the price has been going down
            if stockEODProfile_a_consecutive_days_price_change < 0:
                old_stock_price = current_stock_price + abs(stockEODProfile_a_consecutive_days_price_change)
            # If the price has been going up
            elif stockEODProfile_a_consecutive_days_price_change > 0:
                old_stock_price = current_stock_price - stockEODProfile_a_consecutive_days_price_change
            # If the price remained the same
            else:
                old_stock_price = current_stock_price

            stockEODProfile_q_consecutive_days_percent_change = (stockEODProfile_a_consecutive_days_price_change / old_stock_price) * 100
            stockEODProfile_q_consecutive_days_percent_change = round(stockEODProfile_q_consecutive_days_percent_change, 3)
            ############################################################################################################
            # Volume analysis
            stockEODProfile_q_consecutive_days_volume_growth = 0
            stockEODProfile_a_consecutive_days_volume_change = 0

            current_volume = stockEOD_row[21]
            previous_volume = stockEOD_row[22]

            if current_volume > previous_volume:

                stockEODProfile_q_consecutive_days_volume_growth += 1
                stockEODProfile_a_consecutive_days_volume_change += (current_volume - previous_volume)

                for x in range(23, 28):

                    current_volume = previous_volume
                    previous_volume = stockEOD_row[x]

                    if current_volume > previous_volume:
                        stockEODProfile_q_consecutive_days_volume_growth += 1
                        stockEODProfile_a_consecutive_days_volume_change += (current_volume - previous_volume)
                    else:
                        break
            else:

                stockEODProfile_q_consecutive_days_volume_growth -= 1
                stockEODProfile_a_consecutive_days_volume_change -= (previous_volume - current_volume)

                for x in range(23, 28):

                    current_volume = previous_volume
                    previous_volume = stockEOD_row[x]

                    if current_volume < previous_volume:
                        stockEODProfile_q_consecutive_days_volume_growth -= 1
                        stockEODProfile_a_consecutive_days_volume_change -= (previous_volume - current_volume)
                    else:
                        break

            # Calculate the volume change percentage since the volume started trending down/up
            current_volume = stockEOD_row[21]
            old_volume = 0

            # If the volume has been going down
            if stockEODProfile_a_consecutive_days_volume_change < 0:
                old_volume = current_volume + abs(stockEODProfile_a_consecutive_days_volume_change)
            # If the volume has been going up
            elif stockEODProfile_a_consecutive_days_volume_change > 0:
                old_volume = current_volume - stockEODProfile_a_consecutive_days_volume_change
            # If the volume remained the same
            else:
                old_volume = current_volume

            stockEODProfile_q_consecutive_days_volume_percent_change = (stockEODProfile_a_consecutive_days_volume_change / old_volume) * 100
            stockEODProfile_q_consecutive_days_volume_percent_change = round(stockEODProfile_q_consecutive_days_volume_percent_change, 3)
            ############################################################################################################
            # Calculate the recent close price in relation to the 52 week high and low
            fifty_two_week_high = stockEOD_row[28]
            fifty_two_week_low = stockEOD_row[29]

            stockEODProfile_a_close_to_fifty_two_week_high = (current_stock_price / fifty_two_week_high) * 100
            stockEODProfile_a_close_to_fifty_two_week_high = round(stockEODProfile_a_close_to_fifty_two_week_high, 3)

            stockEODProfile_a_close_to_fifty_two_week_low = (current_stock_price / fifty_two_week_low) * 100
            stockEODProfile_a_close_to_fifty_two_week_low = round(stockEODProfile_a_close_to_fifty_two_week_low, 3)
            ############################################################################################################
            # EPS
            forward_eps = stockEOD_row[30]
            trailing_eps = stockEOD_row[31]
            ############################################################################################################
            # Create the insert query
            stockEODProfile_insert_query = """ INSERT INTO stock_summary_stockeodprofile (stockEOD_id, d_evaluation,
            t_status, a_avg_volume, q_consecutive_days_down, a_consecutive_days_price_change, 
            q_consecutive_days_percent_change, a_close_to_fifty_two_week_high, a_close_to_fifty_two_week_low,
            q_consecutive_days_volume_growth, a_consecutive_days_volume_change, q_consecutive_days_volume_percent_change)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """

            # Create the insert record
            stockEODProfile_insert_record = [stockEODProfile_stockEOD,
                                             stockEODProfile_d_evaluation,
                                             stockEODProfile_t_status,
                                             stockEODProfile_a_avg_volume,
                                             stockEODProfile_q_consecutive_days_down,
                                             stockEODProfile_a_consecutive_days_price_change,
                                             stockEODProfile_q_consecutive_days_percent_change,
                                             stockEODProfile_a_close_to_fifty_two_week_high,
                                             stockEODProfile_a_close_to_fifty_two_week_low,
                                             stockEODProfile_q_consecutive_days_volume_growth,
                                             stockEODProfile_a_consecutive_days_volume_change,
                                             stockEODProfile_q_consecutive_days_volume_percent_change]

            stockEODProfile_insert_record = determine_status(stockEODProfile_insert_record)

            if not debug:
                # Execute the insert statement
                db_cursor.execute(stockEODProfile_insert_query, stockEODProfile_insert_record)

                # Commit the record to the database
                db_connection.commit()

            insert_counter += 1

        except (Exception, psycopg2.DatabaseError) as error:
            error_count += 1
            error_stocks.append(stock[1])
            print(error)
    ####################################################################################################################

    print(data_date, insert_counter, "of", total_stocks_count, "analyzed and inserted successfully")

    if insert_counter == total_stocks_count:
        new_job.job_status = "success"
        new_job.job_message = "processed all stocks successfully"

    # Check for any stocks that had problems processing
    if error_count > 0:

        # Craft email
        subject = "Errors (" + str(error_count) + ") with daily stock data analysis"
        recipient = 'andrew.jacobson22@gmail.com'
        body = ""

        # Iterate through list of errored stocks to craft email body
        for stock in error_stocks:

            body += str(stock) + "\n"

        # Create finished message
        message = "Subject: {}\n\n{}".format(subject, body)

        # Send the email
        stocks_email_config.send_email(recipient, message)

        # Update JobRun object
        new_job.job_status = "error"
        new_job.job_message = str(error_count) + " stocks had issues"

else:

    print(data_date, "was a holiday")

    # Update JobRun object
    new_job.job_status = "holiday"
    new_job.job_message = "holiday yesterday; no data to analyze"

# Insert row for JobRun object
if not debug:
    new_job.insert_job_run()

# Close DB cursor and the connection
stocks_db_config.close_db_cursor(db_cursor)
stocks_db_config.close_connection_to_db(db_connection)
