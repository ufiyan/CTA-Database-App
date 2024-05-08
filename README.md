# CTA-Database-App
The goal of this project is to write a console-based Python program that inputs commands from the user and outputs data from the CTA2 L daily ridership database.
The Updated CTA2 L Daily Ridership Database
The updated CTA2 database consists of 5 tables: Stations, Stops, Ridership, StopDetails, and Lines. This provides information about both stations and stops in the L system.
(It makes use of foreign keys. A foreign key is a primary key stored in another table, typically used to join those tables. You may think of a foreign key as a pointer to the table where it is a primary key.
Example: Station_ID is the primary key of the Stations table, and a foreign key in the Stops and Ridership tables. This allows the Stops and Ridership tables to point to the station name in case it is needed.)
The Stations table denotes the stations on the CTA system. A station can have one or more stops, e.g. “Chicago/Franklin” has 2 stops.
•
Station_ID: primary key, integer
•
Station_Name: string
The Stops table denotes the stops on the CTA system. For example, “Chicago (Loop-bound)” is one of the stops at the “Chicago/Franklin” station. It is a Southbound stop and handicap-accessible (ADA).
•
Stop_ID: primary key, integer
•
Station_ID: the ID of the station that this stop is associated with, foreign key, integer
•
Stop_Name: string
•
Direction: a string that is one of N, E, S, W
•
ADA: integer, 1 if the stop is handicap-accessible, 0 if not
•
Latitude and Longitude: position of the stop, real numbers
