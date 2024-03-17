# youtube_data_harvesting</br>
**Title :** YouTube Data Harvesting and Warehousing using SQL and Streamlit</br>
**Introduction:** Project is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels</br>

**Tools/ Software used:**</br>
Programming language : python (python packages used: googleapiclient, pymongo, pyodbc, pandas, streamlit)</br>
Database : mongodb, MS SQL server Express</br>

**Files:**
1. data_extract.py  : Please update the Youtube **API Key** in this file (line#8). This program is for extracting data from youtube and return channel, video and comment details via Youtube API.
2. mongodbdata.py   : This program is to create database in mongoDB (if not exist) and inset data which was queried from above program. Please update **MongoDB connection detail**s as per your MongoDB setup.
3. sqldata.py       : This program is to create MSSQL Server database and tables to store channel information (if not exist). Update **MSSQLServer Connection details(Line#10-13)**. Extracts channel infromation from mongoDB and migrate to sql server.
4. dataanalysis.py  : This program is for retreiving data from MS sql server based on selected question n Streamlit UI.
5. streamlitapp.py  : This program is to create user interface whcih hosts user actions</br>
----Scrape Youtube channel details based on the user input (input is channel ID) and store the information to MongoDB.</br>
----Migrate data from mongo db to sql server based on the user selected channel name</br>
----Retrieve data from MSSQL Server and display data based on the predefined quesstionnaire</br>
                  
**Project execution :**
1. Setup the environment with the required python packages, MongoDB and MSSQL Server.
2. Execute project by using following command in terminal </br>
command : streamlit run <Full path to streamlitapp.py>
3. Below User interface will be displayed
![image](https://github.com/AnnapurnaBoddu/youtube_data_harvesting/assets/154640492/c8dc0229-3d7e-4f93-9222-d1cfd576002d)
4. User can provide Youtube channel id for whcih the information needs to be fetched from Youtube. Click "scrape" button to extract data from youtube and store it in mongoDB. User can input the multiple channel IDs to scrape but one at a time. Data will be stored in MongoDB
5. Scraped youtube channel ID will be added to the drop down list for SQL Server migration. Select channel to migrate data to sql server and click "migrate" button
6. Predfeined Data nalysis queries would help in fetching information from data migrated to MSSQL server. User is provided a dropdown list with these predeifned questionnaire. Data would be displayed based on teh user selection.
