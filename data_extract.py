import googleapiclient.discovery
import time

api_key = 'AIzaSyDKKGfRaSprUK-uvocdMkWAnx6cN-U9pVQ'
# channel_id = 'UCwCkVWWtpUC-I4YA2qG2Sog'
# for making connection with youtube api
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=api_key)


def channel_details(channel_id):
    """
    This function is used to extract the channel details from youtube api
    :It takes the channel_id as parameter
    :return the channel details
  """

    channel_request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    channel_response = channel_request.execute()

    channel_info = dict(channel_name=channel_response['items'][0]['snippet']['title'],
                        channel_id=channel_response['items'][0]['id'],
                        subscriber_count=channel_response['items'][0]['statistics']['subscriberCount'],
                        channel_views=channel_response['items'][0]['statistics']['viewCount'],
                        channel_description=channel_response['items'][0]['snippet']['description'],
                        video_count=channel_response['items'][0]['statistics']['videoCount'],
                        channel_published=channel_response['items'][0]['snippet']['publishedAt'],
                        playlist_id=channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
    next_page_token = None
    video_info = {}
    j = 1
    while True:
        request1 = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=channel_info['playlist_id'], pageToken=next_page_token
        )
        response1 = request1.execute()
        # pprint(response1)

        # video_info = {}
        n = len(response1['items'])
        # pprint(response1['items'])

        for i in range(n):
            video_id = response1['items'][i]['contentDetails']['videoId']
            # video_info.append(video_details(video_id))
            video_info[f'video_id_{j}'] = video_details(video_id)
            j = j + 1

        next_page_token = response1.get('nextPageToken')

        if next_page_token is None:
            break
        time.sleep(1)
    z = {'channel_name': channel_info, 'videos': video_info}
    return z


def video_details(video_id):
    """
    This function is used to extract the video details from youtube api
    :param video_id:
    :return: video details
    """
    video_request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    video_response = video_request.execute()
    # comment_moderation_status = video_response['items'][0]['snippet'].get('commentsEnabled')

    video_details = dict(video_id=video_response['items'][0]['id'],
                         video_name=video_response['items'][0]['snippet']['title'],
                         video_description=video_response['items'][0]['snippet']['description'],
                         published_at=video_response['items'][0]['snippet']['publishedAt'],
                         view_count=video_response['items'][0]['statistics']['viewCount'],
                         like_count=video_response['items'][0]['statistics'].get('likeCount'),
                         dislike_count=video_response['items'][0]['statistics'].get('dislikeCount'),
                         favorite_count=video_response['items'][0]['statistics']['favoriteCount'],
                         comment_count=video_response['items'][0]['statistics'].get('commentCount'),
                         duration=video_response['items'][0]['contentDetails']['duration'],
                         thumbnail=video_response['items'][0]['snippet']['thumbnails']['medium']['url'],
                         caption_status=video_response['items'][0]['contentDetails']['caption']
                         )

    comments = comment_details(video_details['video_id'])
    video_details['comments'] = comments

    # x = {'videos': video_details, 'comments': comments}
    return video_details


def comment_details(video_id):
    """
    this function extract the comment details from yoytube api
    :param video_id:
    :return: comment details
    """
    comments = []
    next_page_token = None
    try:
        while True:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=10,
                pageToken=next_page_token
            )

            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']

                comments.append(comment)

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break
        z = {}
        # pprint(comments)
        if len(comments) == 0:
            return 'null'
        else:
            # pprint(comments)
            # print(len(comments))
            i = 1
            for com in comments:
                comment = {}
                comment['comment_id'] = com['id']
                comment['comment_text'] = com['snippet']['textDisplay']
                comment['comment_anuthor'] = com['snippet']['authorDisplayName']
                comment['comment_publishedat'] = com['snippet']['publishedAt']
                z[f'comment_id_{i}'] = comment
                i += 1
                if i > 10:
                    break
            return z
    except Exception as e:
        # print(e)
        return 'Null'


# x = channel_details('UCn64faVf-OmarmUn8EsiOLA')
# pprint(x)
# x = comment_details('VaCi5NW-Fv8')
# pprint(x)

def validate_channel(channel_id):
    """
    This function check whether the channel id valid channel id or not
    :param channel_id:
    :return: boolean value
    """
    try:
        # Request channel details
        request = youtube.channels().list(
            part='snippet',
            id=channel_id
        )
        response = request.execute()

        # Check if the response contains valid channel information
        if 'items' in response and len(response['items']) > 0:
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False
