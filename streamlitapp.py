import streamlit as st
from data_extract import channel_details, validate_channel
from mongodbdata import mongodb_data, mongodb_collection_names
from sqldata import insert_record, migrated_channel_list
from dataanlysis import data_analysis

# Project Name
st.header('You Tube Data Harvesting And Warehousing ')
channel_id = st.text_input('Enter your channel id here', placeholder='Enter Channel Id')
if st.button('Scrape') and channel_id:
    if validate_channel(channel_id):
        details = channel_details(channel_id)
        # st.write(details)
        mongo = mongodb_data(details)
        st.write(mongo)
    else:
        st.write('Invalid Channel_id')

collections_list = mongodb_collection_names()
selected_collection = st.selectbox('Select Collection', collections_list, index=None,
                                   placeholder='choose channel to migrate to sql server')
channel_list = migrated_channel_list()
if st.button('migrate') and selected_collection:
    if selected_collection in channel_list:
        st.write('Channel already migrated ')
    else:
        s = insert_record(selected_collection)
        st.write(s)

# data analysis
question_list = ['1. What are the names of all the videos and their corresponding channels?',
                 '2. Which channels have the most number of videos, and how many videos do they have?',
                 '3. What are the top 10 most viewed videos and their respective channels?',
                 '4. How many comments were made on each video, and what are their corresponding video names?',
                 '5. Which video have the highest number of likes, and what are their corresponding channel names?',
                 '6. What is the total number of likes and dislikes for each video, and what are their corresponding '
                 'channel names?',
                 '7. What is the total number of views for each channel, and what are their corresponding channel '
                 'names?',
                 '8. What are the names of all channels that they have published videos in the year 2022?',
                 '9. What is the average duration of all videos in each channel, and what are their corresponding '
                 'channel names?',
                 '10. Which video have the highest number of comments, and what are their corresponding channel names?']
selected_question = st.selectbox('Data Analysis', question_list, index=None, placeholder='choose question')
if selected_question:
    x = data_analysis(selected_question)
    st.table(x)
