import streamlit as st
import pandas as pd

df_m = pd.read_parquet('artist_played_by_month.p')
df_d = pd.read_parquet('artist_played_by_weekday.p')
df_h = pd.read_parquet('artist_played_by_hour.p')

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
