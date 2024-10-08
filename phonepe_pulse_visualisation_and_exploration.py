# ========================================   /  Required Libraries   /   =================================== #
import requests

# SQL and Pandas libraries

import mysql.connector 
import json
import pandas as pd
import numpy as np

# Dash board libraries

import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# ========================================   /   Dash board   /   =================================== #

# Configuring Streamlit GUI

st.set_page_config(page_title="PhonePe Pulse ", page_icon="D:/data science - guvi/MDT-34/capstone project/Project 2 - Phonepe Pulse Data Visualization and Exploration/streamlit images/phonepe-logo-icon.png",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

# Title

st.title(":black[💷 PhonePe Pulse ]")


# Sidebar

with st.sidebar:

    st.markdown("## :violet[Hey Guyss .... Welcome to the Dashboard !!] " )

    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line","exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#9F7ACB"},
                        "nav-link-selected": {"background-color": "#53317B"}})
    
# ========================================   /  Connecting to MySQL database  /   =================================== #   

conn = mysql.connector.connect(host='127.0.0.1',
                               user='root',
                               password='root',
                               database= 'Phonepe_Pulse',
                               auth_plugin='mysql_native_password'
                              )
                                                                                                                                                     
cursor = conn.cursor()  

# ===========================================   / Home Page /   ==========================================  #   

# MENU - HOME

if selected == "Home":

    col1,col2 = st.columns([2,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("#### :violet[**Domain :**]")
        st.markdown("##### FinTech")
        st.markdown("#### :violet[**Skills take away from this Project :**] ")
        st.markdown("#####  Github Cloning, Python, Pandas, MySQL , mysql-connector-python, Streamlit, and Plotly. ")
        st.markdown("#### :violet[**Overall view :**]")
        st.markdown("#####  Building a User-Friendly Streamlit application to visualise and explore Phonepe Pulse Data using Plotly.It is used to gain lots of insights on Transactions, Number of users, Top 10 state, District, Pincode. Bar charts, Pie charts and Geo map visualization are used to get insights.")
        st.markdown("#### :violet[**Developed by :**] ")
        st.markdown("#####  VIDHYALAKSHMI K K")
        
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.video("D:/data science - guvi/MDT-34/capstone project/Project 2 - Phonepe Pulse Data Visualization and Exploration/streamlit images/pulse-video.mp4")

# ===========================================   / Top Charts - Transactions /   ===========================================  #        
  
# MENU - TOP CHARTS

if selected == "Top Charts":

    tab1,tab2 = st.tabs([ "TRANSACTION","🗃 USER"])

    # TOP CHARTS - TRANSACTIONS 

    with tab1:

        st.info(
                """
                ##### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon= "📝"
                )
        
        col1, col2 = st.columns(2)
        with col1:
            Year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='year')
        with col2:
            Quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='quarter')
            
# =============  /  TOP CHARTS - TRANSACTIONS - State   /  ============= #        
 
        r_t=st.radio("**Select the required field**",["State","District","Pincode"],horizontal=True)
        
        if ((Year == '2024') and (Quarter in ['2','3','4']) and (r_t in ["State","District","Pincode"])):
                st.warning(f" Sorry No Data to Display for the year 2024 Quarter {Quarter}", icon="⚠️")
        elif r_t=="State":          
            # State - Bar chart
                st.markdown("### :violet[State]")
                query_1 = f"select State, sum(Transaction_count) as Total_Transaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from Aggregate_Transaction where year = {Year} and quarter = {Quarter} group by state order by Total_Transaction_Amount desc limit 10"
                cursor.execute(query_1)
                df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transaction_Count','Total_Transaction_Amount'])
                df.Total_Transaction_Amount = df.Total_Transaction_Amount.astype(float)

                fig = px.bar(df, x='Total_Transaction_Amount',
                                 y='State',
                                 color='Total_Transaction_Amount',
                                 title='Top 10 States with highest Transaction Amount',
                                 color_continuous_scale=px.colors.sequential.Agsunset,
                                 hover_data=['Total_Transaction_Count'],
                                 labels={'Total_Transaction_Count':'Total_Transaction_Count'},
                                 text_auto='.2s')

                fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True) 
            # State - Data frame
                df.index=df.index+1 
                st.dataframe(df)  
        
                  
# =============  /  TOP CHARTS - TRANSACTIONS - District   /  ============= # 

        elif r_t=="District":     
        # District - Bar chart
                st.markdown("### :violet[District]")
                cursor.execute(f"select district , sum(Transaction_count) as Total_Transaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from Map_Transaction_3 where year = {Year} and quarter = {Quarter} group by district order by Total_Transaction_Amount desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Transaction_Count','Total_Transaction_Amount'])
                df.Total_Transaction_Amount = df.Total_Transaction_Amount.astype(float)
                fig = px.bar(df, x='Total_Transaction_Amount',
                                 y='District',
                                 orientation='h',
                                 color='Total_Transaction_Amount',
                                 title='Top 10 Districts with highest Transaction Amount',
                                 color_continuous_scale=px.colors.sequential.Agsunset,
                                 text_auto='.2s',
                                 hover_data=['Total_Transaction_Count'],
                                 labels={'Total_Transaction_Count':'Total_Transaction_Count'})

                fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)  
        # District - Data frame
                df.index=df.index+1 
                st.dataframe(df) 
       
# =============  /  TOP CHARTS - TRANSACTIONS - Pincode  /  ============= # 

        elif r_t=="Pincode":
                st.markdown("### :violet[Pincode]")
                cursor.execute(f"select Pincode, sum(Pincode_Transaction_count) as Total_Transaction_Count, sum(Pincode_Transaction_amount) as Total_Transaction_Amount from Top_Transaction_Pincode1 where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Transaction_Amount desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transaction_Count','Total_Transaction_Amount'])
                df.Total_Transaction_Amount = df.Total_Transaction_Amount.astype(float)
        
        # Pincode - Bar chart            
                #df['Pincode']= df['Pincode'].astype(str)
                #fig = px.bar(df, x='Pincode',
                #                 y='Total_Transaction_Amount',
                #                 #orientation='h',
                #                 color='Total_Transaction_Amount',
                #                 title='Top 10 Pincodes with highest Transaction Amount',
                #                 color_continuous_scale=px.colors.sequential.Agsunset,
                #                 hover_data=['Transaction_Count'],
                #                 labels={'Transaction_Count':'Transaction_Count'})
                #fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                #fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                #st.plotly_chart(fig,use_container_width=True)

        # Pincode - Pie chart

                fig = px.pie(df, values='Total_Transaction_Amount',
                             names='Pincode',
                             title='Top 10 Pincodes with highest Transaction Amount',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hole=0.3,
                             hover_data=['Transaction_Count'],
                             labels={'Transaction_Count':'Transaction_Count'})   
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)
            
        # Pincode - Data frame
                
                #df.index=df.index+1 
                #st.dataframe(df) 
        else:
            pass        

# ========================================   /  Top Charts - Users /   =================================== #

# MENU - TOP CHARTS      
        
    with tab2:
            r_u=st.radio("**Select the required field**",["Brand","State","District","Pincode"],horizontal=True)

# =============  /  TOP CHARTS - USERS - Brand   /  ============= # 

            # Brand - Bar chart

            if r_u=="Brand":

                st.markdown("### :violet[Brands]")
            
                col1, col2 = st.columns([1,1],gap="large")
                with col1:
                    Year_1 = st.slider("**Year**", min_value=2018, max_value=2022)
                with col2:   
                    Quarter_1 = st.slider("Quarter", min_value=1, max_value=4)
                if ((Year_1 == 2022 )and (Quarter_1 in [2,3,4])):
                    st.warning(f" Sorry No Data to Display for the year 2022 Quarter {Quarter_1}", icon="⚠️")
                else:
                    cursor.execute(f"select Brands, sum(Count_of_users_by_this_brand) as Total_Count_of_users_by_this_brand, avg(percentage) as Average_Percentage from Aggregate_User_brand1 where year = {Year_1} and quarter = {Quarter_1} group by brands order by Total_Count_of_users_by_this_brand desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Count_of_users_by_this_brand','Average_Percentage'])
                    df["Total_Count_of_users_by_this_brand"]=df["Total_Count_of_users_by_this_brand"].astype(float)
                 
                 # Brand - Bar chart    

                    fig = px.bar(df,
                                 title='Top 10 brands with most users',
                                 x="Total_Count_of_users_by_this_brand",
                                 y="Brand",
                                 orientation='h',
                                 color='Total_Count_of_users_by_this_brand',#(try using avg percentage)
                                 color_continuous_scale='Agsunset',
                                 text_auto='.2s')
                    fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                    fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                    st.plotly_chart(fig,use_container_width=True) 

             # Brand - Pie chart
                
                    cursor.execute(f"select Brands, sum(Count_of_users_by_this_brand) as Total_Count_of_users_by_this_brand, avg(percentage)*100 as Average_Percentage from Aggregate_User_brand1 where year = {Year_1} and quarter = {Quarter_1} group by brands order by Total_Count_of_users_by_this_brand desc limit 10;")
                    df1 = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Count_of_users_by_this_brand','Average_Percentage'])
                    df1["Total_Count_of_users_by_this_brand"]=df1["Total_Count_of_users_by_this_brand"].astype(float)
                    fig = px.pie(df1, values='Total_Count_of_users_by_this_brand',
                                     names='Brand',
                                     title='Top 10 brands with most users',
                                     hole=0.3,
                                     color_discrete_sequence=px.colors.sequential.Agsunset,
                                     hover_data=['Average_Percentage'])
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                    st.plotly_chart(fig,use_container_width=True)



# =============  /  TOP CHARTS - USERS - State   /  ============= # 

            if r_u=="State":
                st.markdown("### :violet[State]")
                col1, col2 = st.columns(2)
                with col1:
                    Year_2 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='Year_2',index=3)
                with col2:
                    Quarter_2 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='Quarter_2',index=2)

                # State - Bar chart

                if ((Year_2 == '2024' )and (Quarter_2 in ['2','3','4'])):
                    st.warning(f" Sorry No Data to Display for the year 2024 Quarter{Quarter_2}", icon="⚠️")

                else:
                    cursor.execute(f"select state, sum(Registered_users) as Total_Users, sum(No_of_App_Opens) as Total_App_Opens from map_user where year = {Year_2} and quarter = {Quarter_2} group by state order by Total_Users desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_App_Opens'])
                    df.Total_Users = df.Total_Users.astype(float)
                    fig = px.bar(df, x='Total_Users',
                                     y='State',
                                     orientation='h',
                                     color='Total_Users',
                                     title='Top 10 States with most users',
                                     text_auto='.2s',
                                     color_continuous_scale=px.colors.sequential.Agsunset)

                    fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                    fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                    st.plotly_chart(fig,use_container_width=True)

                # State - Data frame
                    df.index=df.index+1 
                    st.dataframe(df) 

                
# =============  /  TOP CHARTS - USERS - District   /  ============= # 

            if r_u=="District":
                    st.markdown("### :violet[District]")
                    col1, col2 = st.columns(2)
                    with col1:
                        Year_2 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='Year_2',index=3)
                    with col2:
                        Quarter_2 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='Quarter_2',index=2)

                    if ((Year_2 == '2024' )and (Quarter_2 in ['2','3','4'])):
                        st.warning(f" Sorry No Data to Display for the year 2024 Quarter{Quarter_2}", icon="⚠️")   
                    else: 
                        cursor.execute(f"select district, sum(Registered_Users) as Total_Users, sum(No_of_App_Opens) as Total_App_Opens from map_user where year = {Year_2} and quarter = {Quarter_2} group by district order by Total_Users desc limit 10")
                        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_App_Opens'])
                        df.Total_Users = df.Total_Users.astype(float)

                # District - Bar chart        
                        fig = px.bar(df,
                                     title='Top 10 Districts with most users',
                                     x="Total_Users",
                                     y="District",
                                     orientation='h',
                                     text_auto='.2s',
                                     color='Total_Users',
                                     color_continuous_scale=px.colors.sequential.Agsunset)
                        fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                        fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                        st.plotly_chart(fig,use_container_width=True)
                 # District - Data frame
                        df.index=df.index+1 
                        st.dataframe(df) 


# =============  /  TOP CHARTS - USERS -Pincode   /  ============= # 

            if r_u=="Pincode":
                    st.markdown("### :violet[Pincode]")
                    col1, col2 = st.columns(2)
                    with col1:
                        Year_2 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='Year_2',index=3)
                    with col2:
                        Quarter_2 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='Quarter_2',index=2)
                    if ((Year_2 == '2024' )and (Quarter_2 in ['2','3','4'])):
                        st.warning(f" Sorry No Data to Display for the year 2024 Quarter{Quarter_2}", icon="⚠️")
                    else:
                        cursor.execute(f"select Pincode, sum(Pincode_Number_of_registered_users) as Total_Users from Top_User_Pincode where year = {Year_2} and quarter = {Quarter_2} group by Pincode order by Total_Users desc limit 10")
                        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])

                # Pincode - Pie chart

                        fig = px.pie(df,
                                     values='Total_Users',
                                     names='Pincode',
                                     title='Top 10 Pincodes with most users',
                                     hole=0.3,
                                     color_discrete_sequence=px.colors.sequential.Agsunset,
                                     hover_data=['Total_Users'])
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                        st.plotly_chart(fig,use_container_width=True)



# ========================================   /  Explore data - Transaction /   =================================== #

if selected == "Explore Data":

    tab1,tab2 = st.tabs([ "TRANSACTION","🗃 USER"])
    
    with tab1:
        r_t2=st.radio("**Select the required field**",["All India","State","District"],horizontal=True)

# =============  /  EXPLORE DATA - TRANSACTION - All India  /  ============= # 

        if r_t2=="All India":

            st.markdown("### :violet[Transaction Analysis - All India]")

            col1, col2 = st.columns(2)
            with col1:
                year_3 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='in_tr_yr')
            with col2:
                quarter_3 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_tr_qtr')

            if ((year_3 == '2024' )and (quarter_3 in ['2','3','4'])):
                    st.warning(f" Sorry No Data to Display for the year 2022 Quarter {quarter_3}", icon="⚠️")
        # Total Transaction Amount and Transaction count for all States 
            else:
                st.write("") 
                st.write("") 
                st.write("") 

                col1,col2=st.columns(2)
                with col1:
                    st.markdown("##### Total_Payment_Value")
                    query= f"SELECT  sum(Transaction_amount) as Total_Payment_Value from Map_Transaction_3 where year={year_3} AND quarter={quarter_3} "
                    cursor.execute(query)
                    df_3 = pd.DataFrame(np.array(cursor.fetchall()), columns=[ 'Total_Payment_Value']).reset_index(drop=True)
                    st.dataframe(df_3)


                with col2:
                    st.markdown("##### All PhonePe transactions (UPI + Cards + Wallets)")
                    query= f"SELECT  sum(Transaction_count) as Total_Transaction_Count from Map_Transaction_3 where year={year_3} AND quarter={quarter_3} "
                    cursor.execute(query)
                    df_4 = pd.DataFrame(cursor.fetchall(), columns=['Total_Transaction_Count']).reset_index(drop=True)
                    st.dataframe(df_4)

        # GEO VISUALISATION -  Total transaction amount and count for each state

                query= f"SELECT State, sum(Transaction_count) as Total_Transaction_Count, sum(Transaction_amount) as Total_Transaction_Amount  from Map_Transaction_3 where year={year_3} AND quarter={quarter_3} group by State "
                cursor.execute(query)
                df_1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transaction_Count','Total_Transaction_Amount'])

                # Drop a State column from df_1
                df_1.drop(columns=['State'], inplace=True)

                # Clone the gio data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data1 = json.loads(response.content)

                # Extract state names and sort them in alphabetical order
                state_names = [feature['properties']['ST_NM'] for feature in data1['features']]
                state_names.sort()

                 # Create a DataFrame with the state names column
                df_state_names = pd.DataFrame({'State': state_names})

                # Combine the Gio State name with df_1
                df_state_names[['Total_Transaction_Count','Total_Transaction_Amount']]=df_1

                # convert dataframe to csv file
                df_state_names.to_csv('State_names.csv', index=False)

                # Read csv
                df_2 = pd.read_csv('State_names.csv')

                # Geo plot
                fig = px.choropleth(
                                   df_2,
                                   geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                   featureidkey='properties.ST_NM',
                                   locations='State',
                                   color='Total_Transaction_Amount',
                                   color_continuous_scale= px.colors.sequential.Agsunset,
                                   hover_data=['Total_Transaction_Count'],
                                   projection="orthographic",
                                   title="Transaction analysis of States"
                                   )
                fig.update_geos(fitbounds="locations", visible=True,
                                showocean=True, oceancolor="LightBlue")
                fig.update_layout(title_font=dict(size=25),title_font_color='#FFFFFF',height = 700 ,coloraxis_showscale=True,margin={"r":0,"t":100,"l":0,"b":0})
                st.plotly_chart(fig,use_container_width=True)

        # Transaction analysis of states - Bar chart

                df_state_names["Total_Transaction_Amount"]=df_state_names["Total_Transaction_Amount"].astype(float)
                df_sorted = df_state_names.sort_values(by='Total_Transaction_Amount', ascending=False)
                fig = px.bar(df_sorted,
                            title='Transaction analysis of States',
                            y="State",
                            x="Total_Transaction_Amount",
                            orientation='h',
                            text_auto='.2s',
                            color='Total_Transaction_Amount',
                            color_continuous_scale=px.colors.sequential.Agsunset
                            )
                fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                fig.update_layout(title_font_color='#FFFFFF',height = 700,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

        # Transaction Analysis - based on Transaction type

                st.markdown("### :violet[Transaction Analysis - based on Transaction type]")
                type = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services','Others'),key='in_tr_tr_typ')
                query= f"SELECT State, Transaction_count , Transaction_amount from Aggregate_Transaction where year={year_3} AND quarter={quarter_3} AND Transaction_type='{type}' "
                cursor.execute(query)
                df_1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_Count','Transaction_Amount'])

                # GEO VISUALISATION -  based on transaction type

                # Drop a State column from df_1
                df_1.drop(columns=['State'], inplace=True)
    
                # Clone the gio data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data1 = json.loads(response.content)
    
                # Extract state names and sort them in alphabetical order
                state_names = [feature['properties']['ST_NM'] for feature in data1['features']]
                state_names.sort()
    
                 # Create a DataFrame with the state names column
                df_state_names = pd.DataFrame({'State': state_names})
    
                # Combine the Gio State name with df_1
                df_state_names[['Transaction_Count','Transaction_Amount']]=df_1
    
                # convert dataframe to csv file
                df_state_names.to_csv('State_names.csv', index=False)
    
                # Read csv
                df_2 = pd.read_csv('State_names.csv')
    
                # Geo plot
                fig = px.choropleth(
                                   df_2,
                                   geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                   featureidkey='properties.ST_NM',
                                   locations='State',
                                   color='Transaction_Amount',
                                   color_continuous_scale= px.colors.sequential.Agsunset,
                                   hover_data=['Transaction_Count'],
                                   projection="orthographic",
                                   title='Total transaction amount for each transaction type'
                                   )
                fig.update_geos(fitbounds="locations", visible=True,
                                showocean=True, oceancolor="LightBlue")               
                fig.update_layout(title_font=dict(size=25),title_font_color='#FFFFFF',height = 700 ,coloraxis_showscale=True,margin={"r":0,"t":100,"l":0,"b":0})
                st.plotly_chart(fig,use_container_width=True)

        # Total transaction amount for each transaction type - for each year and each quarter - Pie chart
    
                query= f"SELECT Transaction_type , sum(Transaction_count) as Total_Trasaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from Aggregate_Transaction where year={year_3} AND quarter={quarter_3} group by Transaction_type "
                cursor.execute(query)
                df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transaction_Count','Total_Transaction_Amount'])
                fig = px.pie(df,
                             values='Total_Transaction_Amount',
                             names='Transaction_type',
                             title='Total transaction amount for each transaction type',
                             hole=0.3,
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Transaction_Count'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

            
# =============  /  EXPLORE DATA - TRANSACTION - State  /  ============= # 

# Transaction analysis based on Transaction type 
        if r_t2=="State":
            col1_1,col1, col2 = st.columns(3)
            with col1_1:
                state_22 = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'Jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_22')
            with col1:
                year_3 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='in_tr_yr')
            with col2:
                quarter_3 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_tr_qtr')

            if ((year_3 == '2024' )and (quarter_3 in ['2','3','4'])):
                    st.warning(f" Sorry No Data to Display for the year 2022 Quarter {quarter_3}", icon="⚠️")
            else:
                st.write(" ")
                st.write(" ")
                st.write(" ")

                col1_1,col2_1=st.columns(2)
                states={'andaman-&-nicobar-islands':'Andaman and Nicobar', 'andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunachal Pradesh','assam':'Assam', 'bihar':'Bihar', 
                    'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu':'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi':'Delhi', 'goa':'Goa', 'gujarat':'Gujarat', 'haryana':'Haryana', 'himachal-pradesh':'Himachal Pradesh', 
                    'jammu-&-kashmir':'Jammu and Kashmir', 'Jharkhand':'Jharkhand', 'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh','maharashtra':'Maharashtra', 'manipur':'Manipur', 
                    'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland','odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim', 'tamil-nadu':'Tamil Nadu', 'telangana':'Telangana', 
                    'tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh', 'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'

                }
                sta=states[state_22]

                with col1_1:

                    st.markdown("##### Total_Payment_Value")
                    query= f"SELECT  sum(Transaction_amount) as Total_Payment_Value from Map_Transaction_3 where year={year_3} AND quarter={quarter_3} AND state='{sta}' "
                    cursor.execute(query)
                    df_3 = pd.DataFrame(np.array(cursor.fetchall()), columns=[ 'Total_Payment_Value']).reset_index(drop=True)
                    st.dataframe(df_3)


                with col2_1:
                    st.markdown("##### All PhonePe transactions (UPI + Cards + Wallets)")
                    query= f"SELECT  sum(Transaction_count) as Total_Transaction_Count from Map_Transaction_3 where year={year_3} AND quarter={quarter_3} AND state='{sta}' group by state"
                    cursor.execute(query)
                    df_4 = pd.DataFrame(cursor.fetchall(), columns=['Total_Transaction_Count']).reset_index(drop=True)
                    st.dataframe(df_4)

        # Bar chart - Total transaction amount for each transaction type - for each year and each quarter 

                query= f"SELECT Transaction_type , sum(Transaction_count) as Total_Trasaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from Aggregate_Transaction where year={year_3} AND quarter={quarter_3} AND state='{state_22}'  group by State,Transaction_type;"
                cursor.execute(query)
                df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transaction_Count','Total_Transaction_Amount'])
                #fig = px.pie(df,
                #             values='Total_Transaction_Amount',
                #             names='Transaction_type',
                #             title='Total transaction amount for each transaction type',
                #             hole=0.3,
                #             color_discrete_sequence=px.colors.sequential.Agsunset,
                #             hover_data=['Total_Transaction_Count'])
                #fig.update_traces(textposition='outside', textinfo='percent+label')
                #fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True)
                #st.plotly_chart(fig,use_container_width=True)

                df["Total_Transaction_Amount"]=df["Total_Transaction_Amount"].astype(float)
                fig = px.bar(df,
                            title='Total transaction amount for each transaction type',
                            x="Transaction_type",
                            y="Total_Transaction_Amount",
                            color='Total_Transaction_Amount',
                            text_auto='.2s',
                            color_continuous_scale=px.colors.sequential.Agsunset
                            )
                fig.update_traces(textfont_size=16,textangle=0,textposition='outside',text=df['Total_Transaction_Amount'])
                fig.update_layout(title_font_color='#FFFFFF',height = 500,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

        # Pie chart and line graph - Total transaction amount and transaction count for the state - for each year  
                query= f"SELECT state , year ,sum(Transaction_count) as Total_Trasaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from Aggregate_Transaction where  state='{state_22}'  group by State,year; "
                cursor.execute(query)
                df = pd.DataFrame(cursor.fetchall(), columns=['State','Year', 'Total_Transaction_Count','Total_Transaction_Amount'])

                #fig = px.pie(df,
                #             values='Total_Transaction_Count',
                #             names='Year',
                #             title='Total transaction count for each year',
                #             hole=0.3,
                #             color_discrete_sequence=px.colors.sequential.Agsunset,
                #             hover_data=['Total_Transaction_Amount'])
                #fig.update_traces(textposition='inside', textinfo='percent+label')
                #fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True,height=500)
                #st.plotly_chart(fig,use_container_width=True)

                df["Total_Transaction_Amount"]=df["Total_Transaction_Amount"].astype(float)
                fig = px.bar(df,
                            title='Total transaction Amount for each year',
                            x="Year",
                            y="Total_Transaction_Amount",
                            color='Total_Transaction_Amount',
                            hover_data=['Total_Transaction_Amount', 'Total_Transaction_Count'],
                            text_auto='.2s',
                            color_continuous_scale=px.colors.sequential.Agsunset
                            )
                fig.update_traces(textfont_size=16,textangle=0,textposition='outside')
                fig.update_layout(title_font_color='#FFFFFF',height = 500,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

                query= f"SELECT state , quarter ,sum(Transaction_count) as Total_Trasaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from Aggregate_Transaction where  state='{state_22}' AND year={year_3} group by State,quarter; "
                cursor.execute(query)
                df = pd.DataFrame(cursor.fetchall(), columns=['State','Quarter', 'Total_Transaction_Count','Total_Transaction_Amount'])
                fig = px.line(df, x="Quarter", y="Total_Transaction_Count",title=f"Total Transaction count for each quarter in {year_3}",markers=True,color='State',hover_data=["Total_Transaction_Amount"])
                fig.update_layout(title_font_color='#FFFFFF',height = 500,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)


# =============  /  EXPLORE DATA - TRANSACTION - District  /  ============= # 

# Total transaction amount in each district of the state
        if r_t2=="District":
            st.markdown("### :violet[Transaction Analysis - Districts]")
            col5, col6 , col7 = st.columns(3)
            with col5:
                state_1 = st.selectbox('**Select State**',('Andaman and Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 
                'Chandigarh', 'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 
                'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh','Maharashtra', 'Manipur', 
                'Meghalaya', 'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 
                'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'))
            with col6:
                year_7 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='year_7')
            with col7:
                quarter_7 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='quarter_7')

            if ((year_7 == '2024' )and (quarter_7 in ['2','3','4'])):
                    st.warning(f" Sorry No Data to Display for the year 2022 Quarter {quarter_7}", icon="⚠️")
            else:
    # Bar chart for Districts
                query= f"SELECT District, Transaction_count , Transaction_amount from Map_Transaction_3 WHERE State = '{state_1}' AND Year = {year_7} AND quarter ={quarter_7} order by District;"
                cursor.execute(query)
                df_1= pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_count','Transaction_amount'])
                df_1["Transaction_amount"]=df_1["Transaction_amount"].astype(float)
                df_1=df_1.sort_values(by='Transaction_amount',ascending=False)
                fig = px.bar(df_1,
                            title='Transaction analysis of Districts',
                            x="District",
                            y="Transaction_amount",
                            color='Transaction_amount',
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            text_auto='.2s',
                            hover_data=['Transaction_count']
                            )
                fig.update_traces(textfont_size=16,textangle=0, textposition="outside", cliponaxis=False)
                fig.update_layout(title_font_color='#FFFFFF',height = 700,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

    # Geo visualisation for Districts

                gj = json.load(open('India_State_District.geojson',"r"))
                query= f"SELECT District, Transaction_count , Transaction_amount from Map_Transaction_3 WHERE State = '{state_1}' AND Year = {year_7} AND quarter ={quarter_7} order by District;"
                cursor.execute(query)
                df_1= pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_count','Transaction_amount'])
                st.dataframe(df_1)

                # Extract district names and sort them in alphabetical order
                df_1.drop(columns=['District'],axis=1,inplace=True)
                District_names=[]
                for i in gj['features'] :
                    if i['properties']["NAME_1"] == f'{state_1}':
                        District_names.append(i['properties']['NAME_2'])
                District_names.sort()
                df_district_names = pd.DataFrame({'District': District_names})

                # Combine the Gio State name with df_1
                df_district_names[['Transaction_count','Transaction_amount']]=df_1
                # convert dataframe to csv file
                df_district_names.to_csv('district_names.csv', index=False)
                # Read csv
                df_2 = pd.read_csv('district_names.csv')
                fig = px.choropleth(
                                    df_2,
                                    geojson=gj,
                                    featureidkey='properties.NAME_2',
                                    locations='District',
                                    color='Transaction_amount',
                                    color_continuous_scale="Agsunset"
                                    )
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
                st.plotly_chart(fig,use_container_width=True) 
                st.dataframe(df_2)

# ========================================   /  Explore data - Users /   =================================== #
    with tab2:

        r_u2=st.radio("**Select the required Field**",["All India","State","District"],horizontal=True)
        if r_u2=="All India":
            
            col1, col2 = st.columns(2)
            with col1:
                year_4 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='year_4',index=3)
            with col2:
                quarter_4 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='quarter_4',index=2)

            if ((year_4 == '2024' )and (quarter_4 in ['2','3','4'])):
                        st.warning(f" Sorry No Data to Display for the year 2024 Quarter{quarter_4}", icon="⚠️") 
            else:
                st.markdown("### :violet[User Analysis - All India]")
                st.write("") 
                st.write("") 
                st.write("") 

                col3,col4=st.columns(2)
                with col3:
                    st.markdown(f"##### Registered PhonePe users till Q{quarter_4} {year_4}")
                    query= f"SELECT  sum(Registered_Users) as Registered_Users  from Aggregate_User_quarter where year={year_4} AND quarter={quarter_4} "
                    cursor.execute(query)
                    df_3 = pd.DataFrame(cursor.fetchall(), columns=[ 'Registered_Users']).reset_index(drop=True)
                    st.dataframe(df_3)

                with col4:
                    st.markdown(f"##### PhonePe app opens in Q{quarter_4} {year_4}")
                    query= f"SELECT  sum(No_of_App_Opens) as No_of_App_Opens from Aggregate_User_quarter where year={year_4} AND quarter={quarter_4} "
                    cursor.execute(query)
                    df_4 = pd.DataFrame(cursor.fetchall(), columns=['No_of_App_Opens']).reset_index(drop=True)
                    st.dataframe(df_4)

# =============  /  EXPLORE DATA - USERS - All India  /  ============= # 

    #Total Phone users in each state
    
                # Geo visualization 

                query= f"SELECT State, sum(Registered_Users) as Registered_Users, sum(No_of_App_Opens) as App_Opens_in_Q{quarter_4}  from Aggregate_User_quarter where year={year_4} AND quarter={quarter_4} group by State "
                cursor.execute(query)
                df_1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Registered_Users',f'App_Opens_in_Q{quarter_4}'])

                # Drop a State column from df_1
                df_1.drop(columns=['State'], inplace=True)

                # Clone the gio data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data1 = json.loads(response.content)

                # Extract state names and sort them in alphabetical order
                state_names = [feature['properties']['ST_NM'] for feature in data1['features']]
                state_names.sort()

                 # Create a DataFrame with the state names column
                df_state_names = pd.DataFrame({'State': state_names})

                # Combine the Gio State name with df_1
                df_state_names[['Registered_Users',f'App_Opens_in_Q{quarter_4}']]=df_1

                # convert dataframe to csv file
                df_state_names.to_csv('State_names.csv', index=False)
                # Read csv
                df_2 = pd.read_csv('State_names.csv')
                # Geo plot
                fig = px.choropleth(
                                   df_2,
                                   geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                   featureidkey='properties.ST_NM',
                                   locations='State',
                                   color='Registered_Users',
                                   color_continuous_scale= px.colors.sequential.Agsunset,
                                   hover_data=[f'App_Opens_in_Q{quarter_4}'],
                                   projection="orthographic",
                                   title="User analysis of States"
                                   )
                fig.update_geos(fitbounds="locations", visible=True,
                                showocean=True, oceancolor="LightBlue")                      
                fig.update_layout(title_font=dict(size=25),title_font_color='#FFFFFF',height = 700 ,coloraxis_showscale=True,margin={"r":0,"t":100,"l":0,"b":0})
                st.plotly_chart(fig,use_container_width=True)

    # User analysis of states - Bar chart

                df_state_names["Registered_Users"]=df_state_names["Registered_Users"].astype(float)
                df_state_names=df_state_names.sort_values(by="Registered_Users",ascending=False)
                fig = px.bar(df_state_names,
                            title='User analysis of States',
                            x="State",
                            y="Registered_Users",
                            text_auto='.2s',
                            color='Registered_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                fig.update_layout(title_font_color='#FFFFFF',height = 700,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

# =============  /  EXPLORE DATA - USERS - State  /  ============= # 

    # Total Phone users in each quarter of all the districts of the state
        if r_u2=="State":
          
            col5, col6 ,col7 = st.columns(3)
            with col5:
                state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),index=30)

            with col6:
                year_6 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='year_6',index=3)
            with col7:
                quarter_6 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='quarter_6',index=2)
            
            if ((year_6 == '2024' )and (quarter_6 in ['2','3','4'])):
                        st.warning(f" Sorry No Data to Display for the year 2024 Quarter{quarter_6}", icon="⚠️") 
            else:
                st.write("") 
                st.write("") 
                st.write("") 

                col3,col4=st.columns(2)
                with col3:
                    st.markdown(f"##### Registered PhonePe users till Q{quarter_6} {year_6} in {state}")
                    query= f"SELECT  sum(Registered_Users) as Registered_Users  from Map_User_1 where year={year_6} AND quarter={quarter_6} "
                    cursor.execute(query)
                    df_3 = pd.DataFrame(np.array(cursor.fetchall()), columns=[ 'Registered_Users']).reset_index(drop=True)
                    st.dataframe(df_3)

                with col4:
                    st.markdown(f"##### PhonePe app opens in Q{quarter_6} {year_6} in {state}")
                    query= f"SELECT  sum(No_of_App_Opens) as No_of_App_Opens from Map_User_1 where year={year_6} AND quarter={quarter_6} "
                    cursor.execute(query)
                    df_4 = pd.DataFrame(cursor.fetchall(), columns=['No_of_App_Opens']).reset_index(drop=True)
                    st.dataframe(df_4)

                query= f"SELECT state, year ,SUM(Registered_Users) as Registered_Users ,SUM(No_of_App_Opens) as No_of_App_Opens FROM Aggregate_User_quarter WHERE State = '{state}'  GROUP BY State,year;"
                cursor.execute(query)
                df_1 = pd.DataFrame(cursor.fetchall(), columns=['State',"Year" ,'Registered_Users','No_of_App_Opens'])

                # Bar chart

                df_1["Registered_Users"]=df_1["Registered_Users"].astype(int)
                fig = px.bar(df_1,
                            title='User analysis for each year',
                            x="Year",
                            y="Registered_Users",
                            text_auto='.2s',
                            color='Registered_Users',
                            hover_data=['No_of_App_Opens'],
                            color_continuous_scale=px.colors.sequential.Agsunset)
                fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                fig.update_layout(title_font_color='#FFFFFF',height = 500,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

                query= f"SELECT Quarter, SUM(Registered_Users) as Registered_Users ,SUM(No_of_App_Opens) as No_of_App_Opens  FROM Aggregate_User_quarter WHERE State = '{state}' AND Year = {year_6} GROUP BY Quarter;"
                cursor.execute(query)
                df_1 = pd.DataFrame(cursor.fetchall(), columns=['Quarter', 'Registered_Users','No_of_App_Opens'])

                # Bar chart

                df_1["Registered_Users"]=df_1["Registered_Users"].astype(int)
                df_1["Quarter"]=df_1["Quarter"].astype(int)
                fig = px.line(df_1,
                            title='User analysis for each Quarter',
                            x="Quarter",
                            y="Registered_Users",
                            hover_data=['No_of_App_Opens'])
                            #color_continuous_scale=px.colors.sequential.Agsunset)
                fig.update_traces(textfont_size=16,marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                fig.update_layout(title_font_color='#FFFFFF',height = 500,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

                # Pie chart

                fig = px.pie(df_1,
                             values='Registered_Users',
                             names='Quarter',
                             title='User analysis for each Quarter',
                             hole=0.3,
                             hover_data=['No_of_App_Opens'],
                             color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(title_font_color='#FFFFFF',title_font=dict(size=25),coloraxis_showscale=True,height=500)
                st.plotly_chart(fig,use_container_width=True)

# =============  /  EXPLORE DATA - USERS - District  /  ============= # 
       
        if r_u2=="District":
            st.markdown("### :violet[**User Analysis - Districts**]")
            col5, col6 , col7 = st.columns(3)
            with col5:
                state_2 = st.selectbox('**Select State**',('Andaman and Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 
                'Chandigarh', 'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 
                'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh','Maharashtra', 'Manipur', 
                'Meghalaya', 'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 
                'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'),key='state_2',index=30)
            with col6:
                year_8 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='year_8',index=3)
            with col7:
                quarter_8 = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='quarter_8',index=2)
            
            if ((year_8 == '2024' )and (quarter_8 in ['2','3','4'])):
                        st.warning(f" Sorry No Data to Display for the year 2024 Quarter{quarter_8}", icon="⚠️") 
            else:
# User analysis for each district of the state 
                # Bar Chart
                query= f"SELECT District, Registered_Users , No_of_App_Opens from Map_User_1 WHERE State = '{state_2}' AND Year = {year_8} AND quarter ={quarter_8} order by District;"
                cursor.execute(query)
                df_1= pd.DataFrame(cursor.fetchall(), columns=['District', 'Registered_Users','No_of_App_Opens'])

                df_1["Registered_Users"]=df_1["Registered_Users"].astype(float)
                df_1=df_1.sort_values(by="Registered_Users",ascending=False)
                fig = px.bar(df_1,
                            title='User analysis of districts of the State',
                            x="District",
                            y="Registered_Users",
                            color='Registered_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            text_auto='.2s',
                            hover_data=['No_of_App_Opens'])
                fig.update_traces(textfont_size=16,textangle=0, textposition="outside", cliponaxis=False)
                fig.update_layout(title_font_color='#FFFFFF',height = 700,title_font=dict(size=25),coloraxis_showscale=True)
                st.plotly_chart(fig,use_container_width=True)

                # Geo visualisation

                gj = json.load(open('India_State_District.geojson',"r"))
                query= f"SELECT District, Registered_Users , No_of_App_Opens from Map_User_1 WHERE State = '{state_2}' AND Year = {year_8} AND quarter ={quarter_8} order by District;"
                cursor.execute(query)
                df_1= pd.DataFrame(cursor.fetchall(), columns=['District', 'Registered_Users','No_of_App_Opens'])
                df_1.sort_values(by="District",ascending=True)

                df_1.drop(columns=['District'], inplace=True)
                District_names=[]
                for i in gj['features']  :
                    if i['properties']["NAME_1"] == f'{state_2}':
                        District_names.append(i['properties']['NAME_2'])

                District_names.sort(reverse=False)
                df_district_names = pd.DataFrame({'District': District_names})
                # Combine the Gio District name with df_1
                df_district_names[['Registered_Users','No_of_App_Opens']]=df_1
                 # convert dataframe to csv file
                df_district_names.to_csv('district_names.csv', index=False)
                # Read csv
                df_2 = pd.read_csv('district_names.csv')
                fig = px.choropleth(
                                    df_2,
                                    geojson=gj,
                                    featureidkey='properties.NAME_2',
                                    locations='District',
                                    color='Registered_Users',
                                    color_continuous_scale="Agsunset",
                                    projection="orthographic",
                                    hover_data=['No_of_App_Opens'],
                                    title="User analysis of districts of the State"
                                   )
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(title_font=dict(size=25),title_font_color='#FFFFFF',height = 600 ,coloraxis_showscale=True,margin={"r":0,"t":100,"l":0,"b":0})
                st.plotly_chart(fig,use_container_width=True) 

# ===========================================   / About Page /   ==========================================  # 
# MENU - ABOUT

if selected == "About":
        col1,col2 = st.columns([2,3],gap="medium")
        with col1:
            st.write(" ")
            st.write(" ")
            st.markdown("#### :violet[**About PhonePe :**]")
            st.write( "###### <li>PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India.<br><br><li> PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.",unsafe_allow_html=True)
            st.markdown("#### :violet[**About PhonePe Pulse :**]")
            st.write("###### <li>PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.<br><br><li>PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.",unsafe_allow_html=True)

            st.markdown("#### :violet[**About this Application :**]")
            st.write('###### <li>The application extracts data from PhonePe Pulse through GitHub and website.<br><br><li> Then processes the data to obtain insights and information that can be visualized in a user-friendly manner through graphical representation like charts, graphs, and other visual elements .',unsafe_allow_html=True)

            st.markdown("#### :violet[**Inspired from :**]")
            st.write('###### https://www.phonepe.com/pulse/')
        with col2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.image("https://www.phonepe.com/webstatic/7147/static/097755a407bd15c27ffd7889ce80db10/049b4/Icon-1.webp")
            

# ========================================   /  Completed /   =================================== #



