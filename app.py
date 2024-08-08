import streamlit as st
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go

df = pd.read_json('track_data_file0.json', lines=True)
df['date'] = pd.to_datetime(df.endTime).dt.date

df_m = pd.read_parquet('artist_played_by_month.p')
df_d = pd.read_parquet('artist_played_by_weekday.p')
df_h = pd.read_parquet('artist_played_by_hour.p')
df_a = pd.read_parquet('artist_db.p')

st.title("My Spotify")

options = st.multiselect(
    label="Select artists to plot",
    options=df_m['artistName'].unique(),
    default=['Mata', 'Zeus', 'Białas']
)

st.write('Months')
st.bar_chart(df_m[df_m['artistName'].isin(options)], x="yearmonth", y="minsPlayed", color="artistName")

st.write('Days of the week')
st.bar_chart(df_d[df_d['artistName'].isin(options)], x="weekday", y="minsPlayed", color="artistName")

st.write('Hour of the day')
st.bar_chart(df_h[df_h['artistName'].isin(options)], x="hour", y="minsPlayed", color="artistName")

st.header('My top artists & songs', divider='green')


# Format output
format = 'MMM DD, YYYY'

# Calculate the start and end dates
start_date = df['date'].min()
end_date = df['date'].max()
max_days = end_date - start_date

# Create the date range slider
slider = st.slider('Select date', min_value=start_date, value=(start_date, end_date), max_value=end_date, format=format)

# Filter the dataframe based on the slider values
filtered_df = df[(df['date'] >= slider[0]) & (df['date'] <= slider[1])]

# Sort the filtered dataframe and select the top 10 records
top_10_artists = filtered_df.groupby('artistName').sum('msPlayed').sort_values('msPlayed', ascending=False).head(10).reset_index()
top_10_songs = filtered_df.groupby('trackName').sum('msPlayed').sort_values('msPlayed', ascending=False).head(10).reset_index()

images = df_a[df_a['artist_name'].isin(top_10_artists.artistName)]['img_m'][:9]

grid = st.columns(3)
col = 0
for image in images:
    with grid[col]:
        st.image(image)
    col = (col + 1) % 3


# Create two columns
cols = st.columns(2)

my_data = [go.Bar( x = top_10_artists.msPlayed, y = top_10_artists.artistName, orientation = 'h')]
fig = go.Figure(data = my_data)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
cols[0].plotly_chart(fig, key='top_artist', on_select='ignore')


top_songs = [go.Bar( x = top_10_songs.msPlayed, y = top_10_songs.trackName, orientation = 'h')]
fig_songs = go.Figure(data = top_songs)
fig_songs.update_layout(yaxis={'categoryorder':'total ascending'})
cols[1].plotly_chart(fig_songs, key='top songs', on_select='ignore')