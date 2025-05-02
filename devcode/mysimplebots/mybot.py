import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
import datetime
import random
import time



# Sample Data
df=pd.DataFrame()
df['date_str']= pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01']) #pd.date_range('1/1/2011', periods = 5, freq ='M')
df['Category'] = pd.DataFrame(['A', 'B', 'C', 'D', 'E'])
df['Value'] =    pd.DataFrame([10, 20, 15, 30, 25])

print(df)
df['date'] =pd.to_datetime(df['date_str'])
df.drop(columns=['date_str'])

# Streamlit Page Configuration
st.set_page_config(layout="wide")

# --- Top Search Bar ---
# Add search bar
search_term = st.text_input("Search:", placeholder="Enter search term")


# Sidebar for filters
st.sidebar.header("Filters")
# Unique values for each column
unique_col1 = df['Category'].unique()
unique_col2 = df['Value'].unique()
# Multiselect filters
selected_col1 = st.sidebar.multiselect("Category", unique_col1, default=unique_col1)
selected_col2 = st.sidebar.multiselect("Value", unique_col2, default=unique_col2)


df = df[df['Category'].isin(selected_col1) & df['Value'].isin(selected_col2) ]
# df = df[df['Category']==selected_col1 & df['Value']==selected_col2 ]

print('HI..')
# Date slider
# start_date = st.date_input("Start date", min_value=df['date'].min(), max_value=df['date'].max(), value=df['date'].min())
# end_date = st.date_input("End date", min_value=df['date'].min(), max_value=df['date'].max(), value=df['date'].max())

# start_date=df['date'].min()
# end_date=df['date'].max()
# mvalue=df['date'].min()
# today = datetime.date.today().strftime('%Y-%m-%d')
# print('Details are : {} - {} - {} - {}'.format(start_date,end_date,mvalue,today))
# selected_dates = st.slider("Select a date:",min_value=start_date,max_value=end_date,value=datetime.strptime(mvalue, "%Y-%m-%d"),format="YYYY-MM-DD")
# print(f'Selected dates is : {selected_dates}')
# # df = df[(df['date'] >= pd.to_datetime(selected_dates[0])) & (df['date'] <= pd.to_datetime(selected_dates[1])) ]
# print('End..')

#--- Main Content (Left Column) ---
# Create two columns for side-by-side charts
col1, col2, col3 ,col4 = st.columns(4)

#--- Bar Chart (Column 1) ---
with col1:
    # Filter data based on search term
    filtered_data = df[df['Category'].str.contains(search_term, case=False)]
    # Create a bar chart
    fig_bar = px.bar(filtered_data, x='Category', y='Value', title='Bar Chart')
    st.plotly_chart(fig_bar)


#--- Line Chart (Column 1) ---
with col2:
    # Filter data based on search term
    filtered_data = df[df['Category'].str.contains(search_term, case=False)]
    # Create a bar chart
    fig_bar = px.line(filtered_data, x='Category', y='Value', title='Line Chart')
    st.plotly_chart(fig_bar)


#--- Pie Chart (Column 2) ---
with col3:
    # Filter data based on search term
    filtered_data = df[df['Category'].str.contains(search_term, case=False)]
    # Pie chart
    fig_pie = px.pie(filtered_data, values='Value', names='Category', title='Pie Chart')
    st.plotly_chart(fig_pie)


with col4:
    # Hit Counter
    filtered_data = df[df['Category'].str.contains(search_term, case=False)]
    st.metric("Number of Hits-1", len(filtered_data))

with col4:
    # Area Chart
    filtered_data = df[df['Category'].str.contains(search_term, case=False)]
    st.area_chart(filtered_data)

with col4:
    # Scatter Chart
    filtered_data = df[df['Category'].str.contains(search_term, case=False)]
    st.scatter_chart(filtered_data)




#--- Tab for Data and Chat ---
# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["Data Table", "Chat with Bot"])
tab1.write("Your Data Set")
tab1.subheader("Data Table")
filtered_data = df[df['Category'].str.contains(search_term, case=False)]
tab1.table(filtered_data)
def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')
csv_data = convert_df_to_csv(filtered_data)
tab1.download_button(
        label="Download CSV",
        data=csv_data,
        file_name='dataframe.csv',
        mime='text/csv',
    )

tab2.title("Welcome to Bot world")
# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := tab2.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with tab2.chat_message("user"):
        tab2.markdown(prompt)
    # Display assistant response in chat message container
    with tab2.chat_message("assistant"):
        response = tab2.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



