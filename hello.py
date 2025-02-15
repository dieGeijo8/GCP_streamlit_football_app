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

rows = run_query("SELECT * FROM `gcpstreamlitfootball.InjuriesDB.Injuries_SerieA` LIMIT 15")

st.header('Injuries table')

injuries_data = pd.DataFrame(rows)
st.dataframe(injuries_data)