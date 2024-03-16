import pyodbc
import pandas as pd


def data_analysis(question):
        server = r'Purna\SQLEXPRESS'
        database = 'master'
        username = 'sa'
        password = 'sqlserver'
        driver = '{SQL Server}'
        conn = pyodbc.connect(
                'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,autocommit=True)
        cursor = conn.cursor()
        cursor.execute('USE youtube1')


        if question == '1. What are the names of all the videos and their corresponding channels?':
                query = """
                          SELECT c.channel_name, v.video_name FROM channel c 
                            JOIN playlist p ON c.channel_id = p.channel_id
                            JOIN video v ON p.playlist_id = v.playlist_id
                            ORDER BY c.channel_name
                            """
                cursor.execute(query)
                rows = cursor.fetchall()

                data = [{'Channel Name': row.channel_name, 'Video Name': row.video_name} for row in rows]
                df = pd.DataFrame(data)
                return df



        elif question == '2. Which channels have the most number of videos, and how many videos do they have?':
                query = """
                         SELECT c.channel_name, MAX(c.video_count) as number_of_videos 
                         FROM channel c 
                         GROUP BY c.channel_name
                         ORDER BY number_of_videos DESC
                        """
                cursor.execute(query)
                rows = cursor.fetchone()
                data = [{'channel name':rows.channel_name,'number of videos':rows.number_of_videos}]
                df = pd.DataFrame(data)

                return df

        elif question == '3. What are the top 10 most viewed videos and their respective channels?':
            query = """
                    SELECT TOP 10 c.channel_name, v.video_name, v.view_count
                    FROM channel c
                    JOIN playlist p ON c.channel_id = p.channel_id
                    JOIN video v ON p.playlist_id = v.playlist_id
                    ORDER BY v.view_count DESC
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'Channel Name': row.channel_name, 'Video Name': row.video_name, 'view_count': row.view_count} for row in rows]
            df = pd.DataFrame(data)

            return df

        elif question == '4. How many comments were made on each video, and what are their corresponding video names?':
            query = """
                    SELECT v.video_name, COUNT(c.comment_id) AS comment_count
                    FROM video v
                    LEFT JOIN comment c ON v.video_id = c.video_id
                    GROUP BY v.video_name
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'Video Name': row.video_name, 'comment_count': row.comment_count} for row in rows]
            df = pd.DataFrame(data)

            return df

        elif question == '5. Which video have the highest number of likes, and what are their corresponding channel names?':
            query = """
                    SELECT TOP 1 v.video_name, c.channel_name, v.like_count
                    FROM video v
                    JOIN playlist p ON v.playlist_id = p.playlist_id
                    JOIN channel c ON p.channel_id = c.channel_id
                    ORDER BY v.like_count DESC
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'Video Name': row.video_name, 'channel_name': row.channel_name,'like_count': row.like_count} for row in rows]
            df = pd.DataFrame(data)

            return df

        elif question == '6. What is the total number of likes and dislikes for each video, and what are their corresponding channel names?':
            query = """
                           SELECT v.video_name, c.channel_name, ISNULL(v.like_count,0) AS like_count , ISNULL(v.dislike_count,0) AS dislike_count
                           FROM video v
                           JOIN playlist p ON v.playlist_id = p.playlist_id
                           JOIN channel c ON p.channel_id = c.channel_id
                           """
            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)
            data = [{'Video Name': row.video_name, 'channel_name': row.channel_name, 'like_count': row.like_count, 'dislike_count': row.dislike_count} for
                    row in rows]
            df = pd.DataFrame(data)

            return df
        elif question == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
            query = """
                                  SELECT c.channel_name, c.channel_views
                                  FROM channel c
                                  
                                  """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'channel Name': row.channel_name, 'channel_views': row.channel_views} for row in rows]
            df = pd.DataFrame(data)

            return df

        elif question == '8. What are the names of all channels that they have published videos in the year 2022':
            query = """
                                  SELECT distinct c.channel_name
                                  FROM channel c
                                  join playlist p on p.channel_id = c.channel_id
                                  jon video v on v.playlist_id = p.playlist_id
                                  where year(v.published_date) = 2022
                                  

                                  """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'channel_name': row.channel_name} for row in rows]
            df = pd.DataFrame(data)

            return df
        elif question == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
            query = """
                    SELECT c.channel_name, AVG(v.duration) AS average_duration
                    FROM channel c
                    JOIN playlist p ON c.channel_id = p.channel_id
                    JOIN video v ON p.playlist_id = v.playlist_id
                    GROUP BY c.channel_name
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'channel_name': row.channel_name, 'avg duration of videos in seconds': row.average_duration} for
                    row in rows]
            df = pd.DataFrame(data)

            return df
        elif question == '10. Which video have the highest number of comments, and what are their corresponding channel names?':
            query = """
                     SELECT TOP 1 c.channel_name, v.video_name, v.comment_count
                     FROM video v
                     JOIN playlist p ON v.playlist_id = p.playlist_id
                     JOIN channel c ON p.channel_id = c.channel_id
                     ORDER BY v.comment_count DESC
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [{'channel_name': row.channel_name, 'video_name': row.video_name, 'number of comments': row.comment_count} for
                    row in rows]
            df = pd.DataFrame(data)

            return df





        else:
            pass

#x = data_analysis('What is the total number of likes and dislikes for each video, and what are their corresponding channel names?')
#print(x.to_string())



