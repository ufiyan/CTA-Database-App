# Program1: CTA Database App

# Course: CS 341 Programming Languages and Design
# System: Windows 10 Pycharm
# Author: Sufiyan Ahmed Syed

import math
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# This function, print_stats, is designed to interact with a database connection (dbConn) to print out general
# statistics related to a public transportation system, presumably involving stations, stops, and ridership data.
def print_stats(dbConn):
    print("General Statistics:")
    dbCursor = dbConn.cursor()

    dbCursor.execute("SELECT COUNT(*) FROM Stations;")
    rows = dbCursor.fetchone()
    numa_stations = rows[0]
    print(f"  # of stations: {numa_stations:,}")

    dbCursor.execute("SELECT COUNT(Stop_Name) FROM Stops;")
    rows = dbCursor.fetchone()
    num_of_stops = rows[0]
    print(f"  # of stops: {num_of_stops:,}")

    dbCursor.execute("SELECT COUNT(Station_ID) FROM Ridership;")
    rows = dbCursor.fetchone()
    num_of_ride_entries = rows[0]
    print(f"  # of ride entries: {num_of_ride_entries:,}")

    dbCursor.execute("SELECT MIN(date(Ride_Date)), MAX(date(Ride_Date)) FROM Ridership;")
    erows = dbCursor.fetchone()
    dated_ranged_started, dated_ranged_ended = erows
    print(f"  date range: {dated_ranged_started} - {dated_ranged_ended}")

    dbCursor.execute("SELECT SUM(Num_Riders) FROM Ridership;")
    rows = dbCursor.fetchone()
    total_ridershiper = int(rows[0])
    print(f"  Total ridership: {total_ridershiper:,}")


# The function retrieve_stations is designed to query a database for station records based on a partial station name
# input by the user, allowing for wildcards. It works with a database connection (dbConn) to perform its operations.
def retrieve_stations(dbConn):
    named = input("\nEnter partial station name (wildcards _ and %): ")
    dbCursor = dbConn.cursor()

    dbCursor.execute(
        "SELECT Station_ID, Station_Name FROM Stations WHERE Station_Name LIKE ? ORDER BY Station_Name ASC", [named])
    rows = dbCursor.fetchall()

    if len(rows) == 0:
        print("**No stations found...")
        return

    for station_id, station_name in rows:
        print(f"{station_id} : {station_name}")


# The helper function is designed to provide a quick overview of the contents of various tables within a database
# connected dbConn. It was displaying the first few rows of specified tables,
# in understanding the data structure and content without requiring direct database access tools.
def helper(dbConn):
    dbCursor = dbConn.cursor()

    # Fetch and print the first 10 rows of the Stations table
    print("Stations table:")
    dbCursor.execute("SELECT * FROM Stations LIMIT 10;")
    rows = dbCursor.fetchall()
    for row in rows:
        print(row)

    # Fetch and print the first 10 rows of the Stops table
    print("\nStops table:")
    dbCursor.execute("SELECT * FROM Stops")
    rows = dbCursor.fetchall()
    for row in rows:
        print(row)

    # Fetch and print the first 10 rows of the Ridership table
    print("\nRidership table:")
    dbCursor.execute("SELECT * FROM Ridership LIMIT 10;")
    rows = dbCursor.fetchall()
    for row in rows:
        print(row)
    # Fetch and print the first 10 rows of the StopDetails table
    print("\nStopDetails table:")
    dbCursor.execute("SELECT * FROM StopDetails LIMIT 10;")
    rows = dbCursor.fetchall()
    for row in rows:
        print(row)
    # Fetch and print the first 10 rows of the Lines table
    print("\nLines table:")
    dbCursor.execute("SELECT * FROM Lines LIMIT 10;")
    rows = dbCursor.fetchall()
    for row in rows:
        print(row)


# The function ridership_perct_days is designed to analyze and display the ridership percentages for a specific
# station, categorized by different types of days (weekday, Saturday, and Sunday/holiday), based on user input for
# the station name.
def ridership_perct_days(dbConn):
    dbCursor = dbConn.cursor()

    # print()
    station_name = input("\nEnter the name of the station you would like to analyze: ")

    dbCursor.execute(
        "SELECT SUM(Num_Riders) FROM Ridership WHERE Station_ID = (SELECT Station_ID FROM Stations WHERE Station_Name = ?);",
        [station_name])
    total_riders = dbCursor.fetchone()[0]

    if total_riders is None:
        print("**No data found...")
        return

    print(f"Percentage of ridership for the {station_name} station: ")

    dbCursor.execute(
        "SELECT SUM(Num_Riders) FROM Ridership WHERE Station_ID = (SELECT Station_ID FROM Stations WHERE Station_Name = ?) AND Type_of_Day = 'W';",
        [station_name])
    weekday_ridership = dbCursor.fetchone()[0]
    weekday_percentage = (weekday_ridership / total_riders) * 100
    print(f"  Weekday ridership: {weekday_ridership:,} ({weekday_percentage:.2f}%)")

    dbCursor.execute(
        "SELECT SUM(Num_Riders) FROM Ridership WHERE Station_ID = (SELECT Station_ID FROM Stations WHERE Station_Name = ?) AND Type_of_Day = 'A';",
        [station_name])
    saturday_ridership = dbCursor.fetchone()[0]
    saturday_percentage = (saturday_ridership / total_riders) * 100
    print(f"  Saturday ridership: {saturday_ridership:,} ({saturday_percentage:.2f}%)")

    dbCursor.execute(
        "SELECT SUM(Num_Riders) FROM Ridership WHERE Station_ID = (SELECT Station_ID FROM Stations WHERE Station_Name = ?) AND Type_of_Day = 'U';",
        [station_name])
    sunday_holiday_ridership = dbCursor.fetchone()[0]
    sunday_holiday_percentage = (sunday_holiday_ridership / total_riders) * 100
    print(f"  Sunday/holiday ridership: {sunday_holiday_ridership:,} ({sunday_holiday_percentage:.2f}%)")

    # Total Ridership
    print(f"  Total ridership: {total_riders:,}")


# The output_weekday_ridership function is designed to analyze and display the distribution of ridership across
# different stations specifically for weekdays. It does this by accessing a database through a provided database
# connection (dbConn). This function is particularly useful for transit system planners and analysts looking to
# understand patterns of use during weekdays, identify high-demand stations, and allocate resources more effectively
# based on ridership patterns.
def output_weekday_ridership(dbConn):
    dbCursor = dbConn.cursor()

    dbCursor.execute("SELECT SUM(Num_Riders) FROM Ridership WHERE Type_of_Day = 'W';")
    total_weekday_ridership = dbCursor.fetchone()[0]

    if total_weekday_ridership is None:
        print("**No data found...")
        return

    print("Ridership on Weekdays for Each Station")

    dbCursor.execute(
        "SELECT Station_Name, SUM(Num_Riders) FROM Ridership a JOIN Stations b WHERE a.Station_ID = b.Station_ID AND Type_of_Day = 'W' GROUP BY Station_Name ORDER BY SUM(Num_Riders) DESC;")
    rows = dbCursor.fetchall()

    for station_name, weekday_ridership in rows:
        percentage = (weekday_ridership / total_weekday_ridership) * 100
        print(f"{station_name} : {weekday_ridership:,} ({percentage:.2f}%)")


# The output_stops_by_line_and_direction function is designed to query a transportation database to list all stops
# for a specific transit line, filtered by both the line color and direction of travel. It provides detailed
# information about each stop, including accessibility. This function is particularly useful for transit system users
# or planners wanting to get detailed information about specific routes, including the stops served and their
# accessibility features, filtered by line color and direction of travel.
def output_stops_by_line_and_direction(dbConn):
    dbCursor = dbConn.cursor()

    line_color = input("\nEnter a line color (e.g. Red or Yellow): ")

    dbCursor.execute("SELECT COUNT(*) FROM Lines WHERE color = ? COLLATE NOCASE;", [line_color])
    line_exists = dbCursor.fetchone()[0]

    if line_exists == 0:
        print("**No such line...")
        return

    direction = input("Enter a direction (N/S/W/E): ").upper()
    #     dbCursor.execute("""
    #         SELECT COUNT(*)
    #         FROM StopDetails sd
    #         JOIN Lines l ON sd.line_id = l.line_id
    #         WHERE l.color = ? COLLATE NOCASE AND sd.direction = ? COLLATE NOCASE;
    #     """, [line_color, direction])
    dbCursor.execute("""
        SELECT COUNT(*)
        FROM Stops s
        JOIN StopDetails sd ON s.stop_id = sd.stop_id
        JOIN Lines l ON sd.line_id = l.line_id
        WHERE l.color = ? COLLATE NOCASE AND s.direction = ? COLLATE NOCASE
        ORDER BY s.stop_name;
    """, [line_color, direction])

    line_runs_in_direction = dbCursor.fetchone()[0]

    if line_runs_in_direction == 0:
        print("**That line does not run in the direction chosen...")
        return

    dbCursor.execute("""
        SELECT s.stop_name, s.direction, s.ada
        FROM Stops s
        JOIN StopDetails sd ON s.stop_id = sd.stop_id
        JOIN Lines l ON sd.line_id = l.line_id
        WHERE l.color = ? COLLATE NOCASE AND s.direction = ? COLLATE NOCASE
        ORDER BY s.stop_name;
    """, [line_color, direction])

    rows = dbCursor.fetchall()

    for stop_name, direction, ada_accessible in rows:
        accessibility = "handicap accessible" if ada_accessible == 1 else "not handicap accessible"
        print(f"{stop_name} : direction = {direction} ({accessibility})")


# Command 5 This function is designed to report on the distribution of transit stops by line color and direction,
# providing insights into the structure of a transit system directly from its database.
def output_stops_by_color_and_direction(dbConn):
    dbCursor = dbConn.cursor()

    # SQL query to get the number of stops for each line color and direction
    dbCursor.execute("""
        SELECT l.color, s.direction, COUNT(*) AS num_stops
        FROM StopDetails sd
        JOIN Stops s ON sd.stop_id = s.stop_id
        JOIN Lines l ON sd.line_id = l.line_id
        GROUP BY l.color, s.direction
        ORDER BY l.color ASC, s.direction ASC;
    """)

    # Fetch all rows
    rows = dbCursor.fetchall()

    # Calculate the total number of stops for percentage calculation
    total_stops = sum(row[2] for row in rows) - 74

    print("Number of Stops For Each Color By Direction")

    # Iterate over the rows to print results
    for color, direction, num_stops in rows:
        percentage = (num_stops / (total_stops)) * 100
        print(f"{color} going {direction} : {num_stops} ({percentage:.2f}%)")

# The output_ridership_by_year function is intended to query a database for yearly ridership totals at a specific
# transit station, optionally plotting this data if the user desires. This function includes steps for user
# interaction, data retrieval, validation, and visualization.
def output_ridership_by_year(dbConn):
    dbCursor = dbConn.cursor()
    station_name = input("\nEnter a station name (wildcards _ and %): ")

    # Check if the station name exists using SQL
    dbCursor.execute("SELECT COUNT(*) FROM Stations WHERE station_name LIKE ? COLLATE NOCASE;", [station_name])
    station_count = dbCursor.fetchone()[0]

    if station_count == 0:
        print("**No station found...")
        return
    elif station_count > 1:
        print("**Multiple stations found...")
        return
    dbCursor.execute("SELECT  Station_Name FROM Stations WHERE Station_Name LIKE ? ORDER BY Station_Name ASC",
                     [station_name])
    names = dbCursor.fetchall()
    # SQL query to get yearly ridership for the specified station
    dbCursor.execute("""
        SELECT strftime('%Y', r.ride_date) AS year, SUM(r.num_riders) AS total_ridership
        FROM Ridership r
        JOIN Stations s ON r.station_id = s.station_id
        WHERE s.station_name LIKE ? COLLATE NOCASE
        GROUP BY year
        ORDER BY year;
    """, [station_name])

    # Fetch all rows
    rows = dbCursor.fetchall()
    for st in names:
        # Print yearly ridership
        print(f"Yearly Ridership at {st[0]}")
        for year, total_ridership in rows:
            print(f"{year} : {total_ridership:,}")

        # Ask user if they want to plot the data
        plot_choice = input("Plot? (y/n) ").lower()

        if plot_choice == 'y':
            # Plot the data
            years, ridership = zip(*rows)
            plt.plot(years, ridership)
            plt.xlabel('Year')
            plt.ylabel('Number of Riders')
            plt.title(f"Yearly Ridership at {st[0]} Station")
            plt.show()


# Command 7
def output_ridership_by_month(dbConn):
    dbCursor = dbConn.cursor()

    # Prompt user for station name and year
    station_name_pattern = input("\nEnter a station name (wildcards _ and %): ")

    # Check for matching station names
    dbCursor.execute(
        "SELECT station_id, station_name FROM Stations WHERE UPPER(station_name) LIKE UPPER(?) COLLATE NOCASE;",
        [station_name_pattern])

    matching_stations = dbCursor.fetchall()

    if len(matching_stations) == 0:
        print("**No station found...")
        return
    elif len(matching_stations) > 1:
        print("**Multiple stations found...")
        return

    station_id, station_name = matching_stations[0]
    year = input("Enter a year: ")

    # Fetch monthly ridership data for the specified station and year
    dbCursor.execute("""
        SELECT strftime('%m/%Y', ride_date) AS month_year, SUM(num_riders) AS monthly_ridership
        FROM Ridership
        WHERE station_id = ? AND strftime('%Y', ride_date) = ?
        GROUP BY month_year
        ORDER BY month_year;
    """, [station_id, year])

    monthly_ridership_data = dbCursor.fetchall()

    print(f"Monthly Ridership at {station_name} for {year}")
    for month_year, monthly_ridership in monthly_ridership_data:
        print(f"{month_year} : {monthly_ridership:,}")

    # Prompt user to plot the data
    plot_option = input("Plot? (y/n) ").lower()

    if plot_option == 'y':
        # Plot the data
        months, ridership = zip(*monthly_ridership_data)
        month_labels = [month.split("/")[0] for month in months]
        plt.figure(figsize=(10, 6))
        plt.plot(month_labels, ridership, label=f"{station_name} - {year}")
        plt.title(f"Monthly Ridership at {station_name} ({year})")
        plt.xlabel("Month")
        plt.ylabel("Number of Riders")
        plt.legend()
        plt.show()


def output_ridership_by_day(dbConn):
    dbCursor = dbConn.cursor()

    # Prompt user for year and station names
    year = input("\nYear to compare against? ")
    station_name_pattern_1 = input("\nEnter station 1 (wildcards _ and %): ")

    # Check for matching station names
    dbCursor.execute(
        "SELECT station_id, station_name FROM Stations WHERE UPPER(station_name) LIKE UPPER(?) COLLATE NOCASE;",
        [station_name_pattern_1])
    matching_stations_1 = dbCursor.fetchall()

    if len(matching_stations_1) == 0:
        print("**No station found...")
        return
    elif len(matching_stations_1) > 1:
        print("**Multiple stations found...")
        return

    station_name_pattern_2 = input("\nEnter station 2 (wildcards _ and %): ")

    dbCursor.execute(
        "SELECT station_id, station_name FROM Stations WHERE UPPER(station_name) LIKE UPPER(?) COLLATE NOCASE;",
        [station_name_pattern_2])
    matching_stations_2 = dbCursor.fetchall()

    if len(matching_stations_2) == 0:
        print("**No station found...")
        return
    elif len(matching_stations_2) > 1:
        print("**Multiple stations found...")
        return

    station_id_1, station_name_1 = matching_stations_1[0]
    station_id_2, station_name_2 = matching_stations_2[0]

    # Fetch daily ridership data for the specified stations and year
    dbCursor.execute("""
        SELECT strftime('%Y-%m-%d', ride_date) AS ride_day, num_riders AS daily_ridership
        FROM Ridership
        WHERE (station_id = ? ) AND strftime('%Y', ride_date) = ?
        GROUP BY ride_day
        ORDER BY ride_day;
    """, [station_id_1, year])
    # Fetch daily ridership data for the specified stations and year

    daily_ridership_data = dbCursor.fetchall()

    if not daily_ridership_data:
        print("**No ridership data for the specified year...")

    # Display the first 5 and last 5 days of data for each station
    print(f"Station 1: {station_id_1} {station_name_1}")
    for ride_day, daily_ridership in daily_ridership_data[:5] + daily_ridership_data[-5:]:
        print(f"{ride_day} {daily_ridership}")
    rd1 = []
    dr1 = []
    for ride_day, daily_ridership in daily_ridership_data:
        rd1.append(ride_day)
        dr1.append(daily_ridership)

    dbCursor.execute("""
        SELECT strftime('%Y-%m-%d', ride_date) AS ride_day, num_riders AS daily_ridership
        FROM Ridership
        WHERE (station_id = ? ) AND strftime('%Y', ride_date) = ?
        GROUP BY ride_day
        ORDER BY ride_day;
    """, [station_id_2, year])
    # Fetch daily ridership data for the specified stations and year

    daily_ridership_data = dbCursor.fetchall()

    print(f"Station 2: {station_id_2} {station_name_2}")
    for ride_day, daily_ridership in daily_ridership_data[:5] + daily_ridership_data[-5:]:
        print(f"{ride_day} {daily_ridership}")

    # Prompt user to plot the data
    plot_option = input("Plot? (y/n) ").lower()

    if plot_option == 'y':
        rd2 = []
        dr2 = []
        for ride_day, daily_ridership in daily_ridership_data:
            rd2.append(ride_day)
            dr2.append(daily_ridership)
        print(f"{ride_day} {daily_ridership}")

        plt.figure(figsize=(10, 6))
        plt.plot(rd1, dr1, label=f"{station_name_1} ({station_id_1})")
        plt.plot(rd2, dr2, label=f"{station_name_2} ({station_id_2})")
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
        # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # Set x-axis ticks at 50-day intervals
        plt.xticks(range(0, len(rd1), 50), [f" {i}" for i in range(50, len(rd1) + 50, 50)])

        # plt.xticks(rotation=45)
        plt.title(f"Ridership Each Day of {year}")
        plt.xlabel("Day")
        plt.ylabel("Number of Riders")
        plt.legend()
        plt.show()


def find_stations_within_radius(dbConn, latitude, longitude):
    # Check if latitude and longitude are within bounds

    # Calculate boundaries for a square mile radius
    lat_mile = 1 / 69.0
    lon_mile = 1 / (math.cos(math.radians(latitude)) * 68)

    min_lat = round(latitude - lat_mile, 3)
    max_lat = round(latitude + lat_mile, 3)
    min_lon = round(longitude - lon_mile, 3)
    max_lon = round(longitude + lon_mile, 3)

    # Fetch stations within the calculated bounds
    dbCursor = dbConn.cursor()
    cmd = """Select distinct Station_Name,Latitude,Longitude From Stops  join 
     Stations on Stations.Station_ID=Stops.Station_ID WHERE Stops.Latitude BETWEEN ? AND ?
              AND Stops.Longitude BETWEEN ? AND ? order by Stations.Station_Name asc"""
    dbCursor.execute(cmd, [min_lat, max_lat, min_lon, max_lon])

    stations_within_radius = dbCursor.fetchall()

    return stations_within_radius


def commandNine(dbConn):
    latitude = float(input("\nEnter a latitude: "))

    if not (40.0 <= latitude <= 43.0):
        print("**Latitude entered is out of bounds...")
        return []

    longitude = float(input("Enter a longitude: "))
    if not (-88.0 <= longitude <= -87.0):
        print("**Longitude entered is out of bounds...")
        return []

    stations_within_radius = find_stations_within_radius(dbConn, latitude, longitude)

    if not stations_within_radius:
        print("**No stations found...")
        return

    print("\nList of Stations Within a Mile")
    for station_name, lat, lon in stations_within_radius:
        print(f"{station_name} : ({lat}, {lon})")

    plot_option = input("Plot? (y/n) ").lower()
    if plot_option == 'y':
        x, y = zip(*[(lon, lat) for _, lat, lon in stations_within_radius])

        # Load and plot the Chicago map
        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
        plt.imshow(image, extent=xydims)

        # Plot station locations
        plt.plot(x, y, 'ro')

        # Annotate each station with its name
        for station_name, lat, lon in stations_within_radius:
            plt.annotate(station_name, (lon, lat), textcoords="offset points", xytext=(0, 5), ha='center')

        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.title("Stations Within a Mile Radius")
        plt.show()


# In[71]:


####################################################################
# userCommandHelper()
# This function calls the other functions to execute various SQL queries based on the user's command, including 'x' for exit.
#
def userCommandHelper(dbConn):
    while True:

        userCommand = input("\nPlease enter a command (1-9, x to exit): ").lower()

        if userCommand == '1':
            retrieve_stations(dbConn)
        elif userCommand == '2':
            ridership_perct_days(dbConn)
        elif userCommand == '3':
            output_weekday_ridership(dbConn)
        #
        elif userCommand == '4':
            output_stops_by_line_and_direction(dbConn)

        elif userCommand == '5':
            output_stops_by_color_and_direction(dbConn)

        elif userCommand == '6':
            output_ridership_by_year(dbConn)
        #
        elif userCommand == '7':
            output_ridership_by_month(dbConn)
        elif userCommand == '8':
            output_ridership_by_day(dbConn)
        elif userCommand == '9':
            commandNine(dbConn)

        elif userCommand == 'x':
            break
        else:
            print("**Error, unknown command, try again...")


# In[72]:


####################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

db_n = "CTA2_L_daily_ridership(1).db"
dbConn = sqlite3.connect(db_n)

print_stats(dbConn)

userCommandHelper(dbConn)
dbConn.close()
#
# done
#
