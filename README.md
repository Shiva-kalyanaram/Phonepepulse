# PhonepePulse Data Visualization

## Problem Statement
The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner. 

### Project Requirements:
- Extract data from the Phonepe pulse Github repository through scripting and clone it.
- Transform the data into a suitable format and perform any necessary cleaning and pre-processing steps.
- Insert the transformed data into a MySQL database for efficient storage and retrieval.
- Create a live geo visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner.
- Fetch the data from the MySQL database to display in the dashboard.
- Provide at least 10 different dropdown options for users to select different facts and figures to display on the dashboard.

The solution must be secure, efficient, and user-friendly. The dashboard must be easily accessible and provide valuable insights and information about the data in the Phonepe pulse Github repository.

## Utilized Applications and Packages
- Python
- PostgresSql
- Streamlit
- Pandas
- OS
- Github
- Plotly
- Psycopg2

## Approach
To begin my project, I cloned the data from the Phonepe Pulse Github repository to my computer. With the help of the os package, I was able to identify and extract all of the necessary information from all directories & files.

### For Extracting and Cleaning:
Utilized the `json` package to extract information from all the files, which were in Json format, and identified required information.

### For Data Transfer:
Extracted valuable data was uploaded to postgresql with a `pyschopg2` connector in a structured way, and the same mechanism was used for retrieving it back for data visualization.

### Data Visualization:
The `streamlit` Web Application package was used to create a Phonepe overview with five tabs and multiple filtering options to see detailed insight about the data. These tabs include:
- Transaction type and device information
- Geo map visualization
- Top ten states/districts/areas for Phonepe transactions
- User registrations

