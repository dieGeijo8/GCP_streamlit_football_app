import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_file("gcpstreamlitfootball-b7e5d69a75b6.json")
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query('''
SELECT 
  COALESCE(t2.Team_name, 'National team'),
  t3.Player_name,
  Injury, 
  Start_date,
  End_date,
  Games_missed
FROM 
  `gcpstreamlitfootball.InjuriesDB.injuries_complete` t1
LEFT JOIN 
  `gcpstreamlitfootball.InjuriesDB.Teams_SerieA` t2 
ON 
  t1.Team_ID = t2.Team_ID 
LEFT JOIN 
  `gcpstreamlitfootball.InjuriesDB.Players_SerieA` t3 
ON 
  t1.Player_ID = t3.Player_ID''')

st.header('Injuries table')

injuries_data = pd.DataFrame(rows)
st.dataframe(injuries_data)