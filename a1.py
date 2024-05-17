import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title = 'Startup Analysis')

df = pd.read_csv('start_cleaned.csv')

df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():

    total = round(df['amount'].sum())

    #maximum funding on which companies
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding = df.groupby('startup')['amount'].sum().mean()

    #total funded startups

    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max',str(total) + ' Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig_01 , ax_01  = plt.subplots()

    ax_01.plot(temp_df['x-axis'],temp_df['amount'])
    st.pyplot(fig_01)



def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investments of the investor

    last_5df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]

    st.subheader('Most recent investments')
    st.dataframe(last_5df)

    #biggest investment by investors
    col1,col2 = st.columns(2)

    with col1:
         big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
         st.subheader('Biggest investments')
         #st.dataframe(big_df)
         fig , ax  = plt.subplots()

         ax.bar(big_series.index,big_series.values)
         st.pyplot(fig)

         stage_df = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
         st.subheader('Stage invested in')
         #st.dataframe(big_df)
         fig2 , ax2  = plt.subplots()

         ax2.pie(stage_df,labels=stage_df.index,autopct="%0.01f%%")
         st.pyplot(fig2)

    with col2:
         vertical_df = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

         st.subheader('Sectors Invested In')
         #st.dataframe(big_df)
         fig1 , ax1  = plt.subplots()

         ax1.pie(vertical_df,labels=vertical_df.index,autopct="%0.01f%%")
         st.pyplot(fig1)

         city_df = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
         st.subheader('City invested in')
         #st.dataframe(big_df)
         fig4 , ax4  = plt.subplots()

         ax4.pie(city_df,labels=city_df.index,autopct="%0.01f%%")
         st.pyplot(fig4)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig_2, ax_2 = plt.subplots()
    ax_2.plot(year_series.index,year_series.values)

    st.pyplot(fig_2)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis') 
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

    st.title('Investor Analysis')

