from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

st.header('Tony Blood Pressure readings')

st.subheader('Chart of mean readings over time')


trend_interval = 7


def ampm(row):
    if row['time_from_DateTime'] <= 12:
        val = 'am'
    else:
        val = 'pm'
    return val


fpath = 'data/Report (September 23 2022 – October 04 2022).csv'
df = pd.read_csv(fpath, low_memory=False)

# print(df.info())

df['DateTime'] = df.Date.map(str) + " " + df.Time

df['DateTime'] = pd.to_datetime(df['DateTime'], format='%d %b %Y %H:%M')

df['time_from_DateTime'] = df['DateTime'].dt.hour

df['ampm'] = df.apply(ampm, axis=1)


# df = df.set_index('DateTime')


#  Do something with the data
# group by date
# df = df.groupby(df.DateTime.dt.day)["Pulse (bpm)"].mean().reset_index()

df_AM = df[(df.time_from_DateTime >= 0) & (df.time_from_DateTime <= 12)]
# print(df_AM)

df_PM = df[(df.time_from_DateTime > 12) & (df.time_from_DateTime <= 24)]
# print(df_PM)

# calculate equation for trendline
#df_rolling_sys = df['Systolic (mmHg)'].to_frame()


#ampm_filter = 'pm'
#df = df.loc[df['ampm'] == ampm_filter]
df = df.groupby([pd.Grouper(key='DateTime', freq='24H')
                 ]).agg(mean_Pulse=('Pulse (bpm)',
                                    'mean'),
                        mean_BP_Sys=('Systolic (mmHg)',
                                     'mean'),
                        mean_BP_Dia=('Diastolic (mmHg)',
                                     'mean')).reset_index()


df['rolling_sys'] = df['mean_BP_Sys'].rolling(trend_interval).mean()
df['rolling_dia'] = df['mean_BP_Dia'].rolling(trend_interval).mean()

# convert_dict = {'mean_Pulse': int,
#                'mean_BP_Sys': int,
#                'mean_BP_Dia': int}

# df = df.astype(convert_dict)
# need to pull out time only


print(df)


# group by date/time am and pm (12H) done

# Need to split out AM and PM readings to show separate lines on the chart

# Average of lowest two readings?

# Need to Filter reading based on grouping??
# min max of lowest two readings?


# Create a plot or two
# Using a inbuilt style to change
# the look and feel of the plot
plt.style.use("fivethirtyeight")

# setting figure size to 12, 10
fig = plt.figure(figsize=(20, 10))

# Labelling the axes and setting
# a title
plt.xlabel("Date")
plt.ylabel("Values")
plt.title("TD Mean daily blood pressure readings")


plt.plot(df["DateTime"], df["mean_BP_Sys"], label="Systolic", linewidth=1.2, marker='o',
         markerfacecolor='green', markersize=6, alpha=0.7)
plt.plot(df["DateTime"], df["mean_BP_Dia"], label="Diastolic", linewidth=1.2, marker='o',
         markerfacecolor='blue', markersize=6, alpha=0.7)
plt.plot(df["DateTime"], df["mean_Pulse"], label="Pulse", linewidth=1.2, marker='o',
         markerfacecolor='red', markersize=6, alpha=0.7)


plt.plot(df["DateTime"], df["rolling_sys"], label="moving 7 day average",
         linestyle='dashed')
plt.plot(df["DateTime"], df["rolling_dia"], label="moving 7 day average",
         linestyle='dashed')

plt.legend()
plt.show()
st.pyplot(fig)
st.caption('The chart shows seven day rolling average values (dashed lines)')

st.subheader('Readings')

st.dataframe(df)
