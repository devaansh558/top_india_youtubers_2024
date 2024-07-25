import time
import pandas as pd
from googleapiclient.discovery import build
API_KEY = "i got my_api_key from google cloud"  
API_VERSION = 'v3'
youtube = build('youtube', API_VERSION, developerKey=API_KEY)
def get_channel_stats(youtube, channel_id):
    try:
        request = youtube.channels().list(
            part='snippet, statistics',
            id=channel_id
        )
        response = request.execute()
        print(f"Response for {channel_id}: {response}")
        if 'items' in response and response['items']:
            data = dict(
                channel_name=response['items'][0]['snippet']['title'],
                total_subscribers=response['items'][0]['statistics']['subscriberCount'],
                total_views=response['items'][0]['statistics']['viewCount'],
                total_videos=response['items'][0]['statistics']['videoCount']
            )
            return data
        else:
            print(f"Channel ID {channel_id} not found or invalid response.")
            return None
    except Exception as e:
        print(f"An error occurred for Channel ID {channel_id}: {e}")
        return None
df = pd.read_csv("/content/youtube_data_india.csv")
df['channel_id'] = df['NAME'].str.split('@').str[-1].str.strip()  # Strip any extra whitespace
channel_ids = df['channel_id'].unique()
channel_stats = []
# Loop over the channel IDs and get stats for each
for channel_id in channel_ids:
    print(f"Processing Channel ID: {channel_id}")  # Debugging line
    stats = get_channel_stats(youtube, channel_id)
    if stats is not None:
        channel_stats.append(stats)
    time.sleep(1)  # Add a delay to avoid hitting rate limits
stats_df = pd.DataFrame(channel_stats)
combined_df = pd.concat([df.reset_index(drop=True), stats_df.reset_index(drop=True)], axis=1)
combined_df.to_excel('updated_youtube_data_india.xlsx', index=False) 

 
 
