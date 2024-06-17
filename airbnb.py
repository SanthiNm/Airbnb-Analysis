import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px # type: ignore
from streamlit_option_menu import option_menu # type: ignore
from PIL import Image

# Setting up page configuration


st.set_page_config(page_title= "Airbnb Data Visualization | By Jafar Hussain",
                   page_icon="🧊",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items = None)



with st.sidebar:
     st.title(":red[Airbnb ANALYSIS]")
     select = option_menu(":Menu",["Home","Overview","Data Exploration"],
                          icons = ["house","bar-chart","info-circle"],
                          )
     


# HOME PAGE
if select == "Home":
     
     col1,col2 = st.columns(2, gap = 'medium')
    
     with col1:
            
          col1.markdown("## :red[Data from]: Airbnb|Holiday rentals,cabins,beach houses & more") 
          url = "https://www.airbnb.co.in/"
          
          col1.markdown("Know more about us [link](%s)" % url)
          
          col1.markdown("### :red[Domain] : Travel Industry, Property Management and Tourism")
          col1.markdown("### :red[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")

     with col2:
         
          image = Image.open("C:/Users/santh/Desktop/Capstone Projects/New folder/PROJECTS/airbnb_analysis/Airbnb-logo.png")
          new_image = image.resize((300,200))
          st.image(new_image)

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://Santhi:santhikichu@cluster0.jwz3noh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.Airbnb_Analysis
col = db.data


# READING THE CLEANED DATAFRAME
df = pd.read_csv('airbnb_sample_data.csv')

# OVERVIEW PAGE
if select == "Overview":

      if st.button("Click to view Sample data"):
        st.write(df.head(25))

# DATA EXPLORATION 
if select == "Data Exploration":
      col1,col2 = st.columns(2, gap = 'medium')
      with col1:
          country = st.multiselect('Select a Country',sorted(df.country.unique()),sorted(df.country.unique()))
          prop = st.multiselect('Select Property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
          room = st.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
          price = st.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))

      with col2:
           
           query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
           
           options = ["a.TOP 10 PROPERTY TYPES BAR CHART",
                       "b.TOP 10 HOSTS BAR CHART",
                       "c.AVERAGE PRICE BY ROOM TYPE BARCHART",
                       "d.AVAILABILITY BY ROOM TYPE BOX PLOT"]
           
           category = st.selectbox("Select the category",options)

           if category == "a.TOP 10 PROPERTY TYPES BAR CHART":

               # TOP 10 PROPERTY TYPES BAR CHART
               
               df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
               fig = px.bar( df1,
                              title='Top 10 Property Types',
                              x='Listings',
                              y='property_type',
                              orientation='h',
                              color='property_type',
                              color_continuous_scale=px.colors.sequential.Agsunset)
               st.plotly_chart(fig,use_container_width=True) 
          
           elif category == "b.TOP 10 HOSTS BAR CHART":

               # TOP 10 HOSTS BAR CHART
               df2 = df.query(query).groupby(["host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
               fig = px.bar(df2,
                              title='Top 10 Hosts with Highest number of Listings',
                              x='Listings',
                              y='host_name',
                              orientation='h',
                              color='host_name',
                              color_continuous_scale=px.colors.sequential.Agsunset)
               fig.update_layout(showlegend=False)
               st.plotly_chart(fig,use_container_width=True)

           elif category == "c.AVERAGE PRICE BY ROOM TYPE BARCHART":
               # AVG PRICE BY ROOM TYPE BARCHART
               pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
               fig = px.bar(data_frame=pr_df,
                         x ='room_type',
                         y ='price',
                         color='price',
                         title='Avg Price in each Room type'
                         )
               st.plotly_chart(fig,use_container_width=True)
           
           elif category == "d.AVAILABILITY BY ROOM TYPE BOX PLOT":
               # AVAILABILITY BY ROOM TYPE BOX PLOT
               fig = px.box(data_frame=df.query(query),
                         x='room_type',
                         y='availability_365',
                         color='room_type',
                         title='availability by Room_type'
                         )
               st.plotly_chart(fig,use_container_width=True)