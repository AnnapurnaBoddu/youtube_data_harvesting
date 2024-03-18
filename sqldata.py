from pymongo import MongoClient
import pyodbc
from isodate import parse_duration
import datetime


def sql_schemadef():
    """
    This function is to create database and tables (channel,playlist, video, comment)
    :return: None
    """
    # creating data base
    server = r'Purna\SQLEXPRESS'
    database = 'master'
    username = 'sa'
    password = 'sqlserver'
    driver = '{SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
        autocommit=True)
    cursor = conn.cursor()
    new_database_name = 'youtube1'
    cursor.execute('CREATE DATABASE ' + new_database_name)

    cursor.execute('USE youtube1')

    # creating tables
    sql_create_channel_table = '''
    CREATE TABLE channel (
        channel_id VARCHAR(255) PRIMARY KEY,
        channel_name VARCHAR(255),
        channel_views INT,
        channel_description TEXT,       
        channel_published DATETIME,
        subscriber_count INT,
        video_count INT,       
    )
    '''
    cursor.execute(sql_create_channel_table)

    sql_create_playlist_table = '''
        CREATE TABLE playlist (
           playlist_id VARCHAR(255) PRIMARY KEY,
           channel_id VARCHAR(255),
           FOREIGN KEY (channel_id) REFERENCES channel(channel_id)                 
        )
        '''
    cursor.execute(sql_create_playlist_table)

    sql_create_video_table = '''
            CREATE TABLE video (
                video_id VARCHAR(255) PRIMARY KEY,
                playlist_id VARCHAR(255) ,
                video_name VARCHAR(255),
                video_description TEXT,
                published_date DATETIME,
                view_count INT,
                like_count INT,
                dislike_count INT,
                favorite_count INT,
                comment_count INT,
                duration INT,
                thumbnails VARCHAR(255),
                caption_status VARCHAR(255),
                FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)      
            )
            '''
    cursor.execute(sql_create_video_table)

    sql_create_comment_table = '''
        CREATE TABLE comment (
            comment_id VARCHAR(255) PRIMARY KEY,
            video_id VARCHAR(255),
            comment_text TEXT,
            comment_author VARCHAR(255),
            comment_published_date DATETIME ,
            FOREIGN KEY (video_id) REFERENCES video(video_id)              
        )
        '''
    cursor.execute(sql_create_comment_table)

    conn.close()


def insert_record(channel_name):
    """
    This function to extract data from mongodb and insert into sql server based on channel name
    :param channel_name:
    :return: string value
    """
    # establish connectio to mongodb
    mongo_client = MongoClient('mongodb://localhost:27017/')

    # sql server connection
    server = r'Purna\SQLEXPRESS'  # Server name or IP address
    database = 'master'  # Default database (system database)
    username = 'sa'  # Username
    password = 'sqlserver'  # Password
    driver = '{SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
        autocommit=True)
    cursor = conn.cursor()

    # SQL query to check if the database exists
    sql_query = "SELECT name FROM sys.databases WHERE name = ?"
    cursor.execute(sql_query, 'youtube1')
    row = cursor.fetchone()
    if row is None:
        sql_schemadef()
    cursor.execute('USE youtube1')

    mongo_db = mongo_client['youtube']
    mongo_collection = mongo_db[channel_name]
    mongo_data = mongo_collection.find_one({})
    # pprint.pprint(mongo_data['videos'])
    # video = list(mongo_data['videos'])
    # pprint.pprint((mongo_data['videos'].items()))
    # for channel data

    date_time_str = mongo_data['channel_name']['channel_published']

    # Convert string to datetime object
    try:
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    channel_data = (mongo_data['channel_name']['channel_id'], mongo_data['channel_name']['channel_name'],
                    mongo_data['channel_name']['channel_views'], mongo_data['channel_name']['channel_description'],
                    date_time_obj, mongo_data['channel_name']['subscriber_count'],
                    mongo_data['channel_name']['video_count'])
    query = """
            INSERT INTO channel (
                channel_id, channel_name, channel_views, channel_description,
                channel_published, subscriber_count, video_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    cursor.execute(query, channel_data)

    # for playlist data
    playlist_data = (mongo_data['channel_name']['playlist_id'], mongo_data['channel_name']['channel_id'])
    query1 = """
             INSERT INTO playlist (playlist_id,channel_id) 
             VALUES (?,?)
            """
    cursor.execute(query1, playlist_data)

    # video data and comment data

    video_data = mongo_data['videos']
    for video_id, video_info in video_data.items():
        # access video data
        duration_str = video_info['duration']
        duration_seconds = parse_duration(duration_str).total_seconds()
        date_time_str1 = video_info['published_at']

        # Convert string to datetime object
        try:
            date_time_obj1 = datetime.datetime.strptime(date_time_str1, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            date_time_obj1 = datetime.datetime.strptime(date_time_str1, '%Y-%m-%dT%H:%M:%S.%fZ')

        video = (video_info['video_id'], mongo_data['channel_name']['playlist_id'], video_info['video_name'],
                 video_info['video_description'], date_time_obj1, video_info['view_count'],
                 video_info['like_count'], video_info['dislike_count'], video_info['favorite_count'],
                 video_info['comment_count'], duration_seconds, video_info['thumbnail'],
                 video_info['caption_status'])

        query2 = """
                 INSERT INTO video (
                                video_id, playlist_id, video_name, video_description, published_date, view_count, 
                                like_count, dislike_count, favorite_count, comment_count, duration, thumbnails,
                                caption_status
                 )
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                 """
        cursor.execute(query2, video)
        # Access comments data for each video
        comments_data = video_info.get('comments', {})
        if isinstance(comments_data, dict):
            for comment_id, comment_info in comments_data.items():
                date_time_str2 = comment_info['comment_publishedat']

                # Convert string to datetime object
                try:
                    date_time_obj2 = datetime.datetime.strptime(date_time_str2, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    date_time_obj2 = datetime.datetime.strptime(date_time_str2, '%Y-%m-%dT%H:%M:%S.%fZ')
                comment_details = (
                    comment_info['comment_id'],
                    video_info['video_id'],
                    comment_info['comment_text'],
                    comment_info['comment_anuthor'],
                    date_time_obj2
                )
                query3 = """
                        INSERT INTO comment ( comment_id, video_id, comment_text, comment_author, comment_published_date
                        )
                        VALUES (?,?,?,?,?)
                        """
                cursor.execute(query3, comment_details)
    conn.close()
    return 'Successfully Migrated'


def migrated_channel_list():
    server = r'Purna\SQLEXPRESS'  # Server name or IP address
    database = 'master'  # Default database (system database)
    username = 'sa'  # Username
    password = 'sqlserver'  # Password
    driver = '{SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
        autocommit=True)
    cursor = conn.cursor()
    # check database exist or not
    sql_query = "SELECT name FROM sys.databases WHERE name = ?"
    cursor.execute(sql_query, 'youtube1')
    row1 = cursor.fetchone()
    if row1 is None:
        conn.close()
        return None
    else:
        cursor.execute('USE youtube1')
        query = 'SELECT c.channel_name FROM channel c'
        cursor.execute(query)
        rows = cursor.fetchall()
        channel_names = [row.channel_name for row in rows]
        conn.close()
        return channel_names
