import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import plotly.express as px

# BigQuery API client.
credentials = service_account.Credentials.from_service_account_file("")
client = bigquery.Client(credentials=credentials)

# Function to the get and cache the data
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

# SQL query
rows = run_query('''
SELECT 
  COALESCE(t2.Team_name, 'National team') as Team_name,
  t3.Player_name,
  Injury, 
  Start_date,
  End_date,
  Games_missed
FROM 
  `gcpstreamlitfootball.InjuriesDB.Injuries_SerieA` t1
LEFT JOIN 
  `gcpstreamlitfootball.InjuriesDB.Teams_SerieA` t2 
ON 
  t1.Team_ID = t2.Team_ID 
LEFT JOIN 
  `gcpstreamlitfootball.InjuriesDB.Players_SerieA` t3 
ON 
  t1.Player_ID = t3.Player_ID''')

injuries_df = pd.DataFrame(rows)
injuries_df = injuries_df.drop_duplicates()


st.header('Injuries Serie A 2023-2024')
st.markdown('''
### **About the Data**
The data displayed is scraped from **Transfermarkt**, focusing on injuries that occurred to Serie A players during the **2023/2024 season**. You can access the scraping code used to gather this data on [GitHub](https://github.com/dieGeijo8/Transfermarkt_DB_WSL).

### **Project Overview**
This application is part of a project that aims to analyze and visualize player injury data using **Streamlit** and **GCP**. The full project and its source code are available on [GitHub](https://github.com/dieGeijo8/GCP_streamlit_football_app).

### **Features**
- The app provides various **grouping options** to explore the data.
- A **line chart** visualizes the evolution of injuries throughout the season.
- You can interact with the displayed tables to **sort**, **download**, and explore the data further.
''')

st.divider()

st.markdown('''
### **Injuries aggregations**
Explore the data looking at the original table and different grouping options.''')


# Initialize session state for toggling
if "show_grouped_team" not in st.session_state:
    st.session_state.show_grouped_team = False
if "show_grouped_player" not in st.session_state:
    st.session_state.show_grouped_player = False
if "show_grouped_injury" not in st.session_state:
    st.session_state.show_grouped_injury = False

# Toggle functions (ensuring only one grouping is active)
def grouping_team():
    st.session_state.show_grouped_team = not st.session_state.show_grouped_team
    st.session_state.show_grouped_player = False
    st.session_state.show_grouped_injury = False

def grouping_player():
    st.session_state.show_grouped_player = not st.session_state.show_grouped_player
    st.session_state.show_grouped_team = False
    st.session_state.show_grouped_injury = False

def grouping_injury():
    st.session_state.show_grouped_injury = not st.session_state.show_grouped_injury
    st.session_state.show_grouped_team = False
    st.session_state.show_grouped_player = False

# Buttons in same row
col1, col2, col3, _ = st.columns([2, 2, 2, 2])
with col1:
    st.button("Group by Team", on_click=grouping_team)
with col2:
    st.button("Group by Player", on_click=grouping_player)
with col3:
    st.button("Group by Injury", on_click=grouping_injury)

# Display grouped data or original data
if st.session_state.show_grouped_team:
    grouped_by_team = injuries_df.groupby("Team_name").agg(
        Count=("Team_name", "count"),
        Sum=("Games_missed", "sum")
    ).reset_index().rename(columns={"Count": "N. of injuries", "Sum": "N. of games missed"})
    st.dataframe(grouped_by_team)

elif st.session_state.show_grouped_player:
    grouped_by_player = injuries_df.groupby("Player_name").agg(
        Count=("Player_name", "count"),
        Sum=("Games_missed", "sum")
    ).reset_index().rename(columns={"Count": "N. of injuries", "Sum": "N. of games missed"})
    st.dataframe(grouped_by_player)

elif st.session_state.show_grouped_injury:
    grouped_by_injury = injuries_df.groupby("Injury").agg(
        Count=("Injury", "count"),
        Sum=("Games_missed", "sum")
    ).reset_index().rename(columns={"Count": "N. of injuries", "Sum": "N. of games missed"})
    st.dataframe(grouped_by_injury)

else:
    st.dataframe(injuries_df)

st.divider()

st.markdown('''
### **Injuries over the season**
Explore the number of injuries over the different weeks and months of the season.''')

# Initialize session state for toggle
if "group_by_month" not in st.session_state:
    st.session_state.group_by_month = False  # Default to weekly aggregation

col1, col2, col3 = st.columns([2, 2, 4])
# Allow the user to select the date range
with col1:
    start_date = st.date_input("Select start date", value=pd.to_datetime("2024-01-01"))
with col2:
    end_date = st.date_input("Select end date", value=pd.to_datetime("2024-02-28"))

# Toggle button to switch between weekly and monthly aggregation
if st.button("Group by Week/Month"):
    st.session_state.group_by_month = not st.session_state.group_by_month

# Filter the DataFrame based on the selected date range
injuries_df_filtered = injuries_df[
    (injuries_df['Start_date'] >= start_date) & (injuries_df['End_date'] <= end_date)
]

if not injuries_df_filtered.empty:
    period_injuries = []

    for _, row in injuries_df_filtered.iterrows():
        if st.session_state.group_by_month:
            date_range = pd.date_range(row['Start_date'], row['End_date'], freq='MS')
        else:
            date_range = pd.date_range(row['Start_date'], row['End_date'], freq='W-MON')

        for date in date_range:
            period_injuries.append(date)

    period_df = pd.DataFrame(period_injuries, columns=["Injury_date"])

    period_counts = period_df.groupby("Injury_date").size().reset_index(name="Injuries")

    # Create the line chart using Plotly Express
    period_type = "Month" if st.session_state.group_by_month else "Week"
    fig = px.line(period_counts, x="Injury_date", y="Injuries",
                  title=f"Number of Injuries per {period_type}",
                  labels={"Injury_date": f"{period_type}", "Injuries": "Number of Injuries"})
    fig.update_xaxes(tickangle=45)  # Rotate the x-axis labels for better readability
    st.plotly_chart(fig)

else:
    st.write("No data available for the selected date range.")