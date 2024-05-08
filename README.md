# CTA2 L Daily Ridership Database Analysis App
# Overview
This project is a console-based Python application that retrieves and analyzes data from the CTA2 L daily ridership database. It utilizes SQL for data extraction and computation, while Python is used for user commands, data display, and optional data visualization via plots. The app provides users with insightful analytics on Chicago's CTA L system.

# Database Structure
The CTA2 database comprises five tables: Stations, Stops, Ridership, StopDetails, and Lines. The key relationships include:

Stations: Contains station identifiers and names.
Stops: Stores details of individual stops, including station association, direction, and accessibility.
Ridership: Details daily ridership figures, categorized by day type.
StopDetails: Links stops to the lines they serve.
Lines: Represents the CTA line colors.
Key Features
General Statistics: Displays an overview of the CTA L system's ridership data, including station, stop, and entry counts.
Command Interface: The command-loop interface accepts commands (1-9, x to exit) to execute various data queries:
Command 1: Search for station names matching a user-provided pattern.
Command 2: Retrieve ridership percentages by weekday, Saturday, and Sunday/holiday for a specific station.
Command 3: Display weekday ridership totals for each station.
Command 4: List stops of a specific line by direction.
Command 5: Count and categorize stops by line color and direction.
Command 6: Show yearly ridership trends for a specific station.
Command 7: Provide monthly ridership data for a specific station in a given year.
Command 8: Compare daily ridership data between two stations.
Command 9: Identify stations within a one-mile radius of specified coordinates.

# Requirements
Python 3: The application uses Python for user interaction and data visualization.
SQLite3: SQL queries are executed through the sqlite3 package for efficient data computation.
Matplotlib: Optional plotting capabilities are implemented via Matplotlib.
Ensure you follow good programming practices with functions and comments to maintain code clarity and organization. Enjoy analyzing Chicago's CTA L system with this intuitive tool!
