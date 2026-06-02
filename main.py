import streamlit as st 
import plotly.graph_objects as go 
import sqlite3 
import json
from datetime import date, timedelta, datetime

# Page configuration
st.set_page_config(
    page_title = "Activity Tracker",
    page_icon = "📊",
    layout = "wide",
    initial_sidebar_state= "collapsed"
)

# CONSTANTS
TASKS = [
    "Bible Study",
    "Pre-Market Prep",
    "Trading Sessions",
    "Study Block",
    "Focus Time",
    "Gym",
]