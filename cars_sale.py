#Author: Ravish Garg
#Customer Engineer, Data Specialist

import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import pandas.io.sql as sqlio
import pandasql as ps
import os, io, cv2, sys, re
from datetime import datetime
import psycopg2
import math

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

st.set_page_config(page_title='GCP DEMO - Cars 4 Sale', page_icon=':smiley:')

page_bg_img = """
<style>
.reportview-container {
background-image: linear-gradient(rgba(0, 0, 0, 0.7),
                       rgba(0, 0, 0, 0.7)),url("https://images.unsplash.com/photo-1621831955776-6ce162d24933?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80");
background-size: cover;
}
.sidebar .sidebar-content {
   display: flex;
   align-items: center;
   justify-content: center;
}
</style>
"""
#st.markdown(page_bg_img, unsafe_allow_html=True


def inventory():
    st.write("#### Cars at best prices...")
    conn = psycopg2.connect(host='35.240.192.226', port=5435, dbname='users', user='postgres', password='ravish')
    sql = "select * from car_details;"
    dat = sqlio.read_sql_query(sql, conn)
    conn = None
    #st.dataframe(dat)
    #<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    card_template = """
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                        <div class="card bg-light mb-3" >
                            <H5 class="card-header">{}.  <a href={} style="display: inline-block" target="_blank">{}</h5>
                                <div class="card-body">
                                    <span class="card-text"><b>Year: </b>{}</span><br/>
                                    <span class="card-text"><b>Selling_Price (INR): </b>{}</span><br/>
                                    <span class="card-text"><b>Owner: </b>{}</span><br/>
                                    <span class="card-text"><b>Seller_Type: </b>{}</span><br/>
                                    <span class="card-text"><b>Mileage (kmpl): </b>{}</span><br/>
                                    <span class="card-text"><b>Transmission: </b>{}</span><br/><br/>
                                    <p class="card-text"><b>No. of seats: </b>{}
                                    <b>,Max_power (bhp): </b>{}
                                    <b>,KM Driven: </b>{}
                                    <b>,Fuel: </b>{}
                                    <b>,Estimated Price: </b>{}
                                    </p>
                                </div>
                            </div>
                        </div>
            """
    #paper_url='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
    paper_url=''
    for index, row in dat.iloc[8120:].iterrows():
        st.markdown(card_template.format(str(index + 1), paper_url, row['name'], row['year'], row['selling_price'], row['owner'], row['seller_type'], row['mileage'], row['transmission'], row['seats'], row['max_power'], row['km_driven'], row['fuel'], row['predicted_selling_price']), unsafe_allow_html=True)        
    #conn.close()

def sell_car():
    st.write("## Provide your car details:")
    name = str(st.text_input("Car Model Name: "))
    year = int(st.slider("Year: ",1990,2022,2015))
    km_driven = int(st.number_input("KM Driven: "))
    fuel = str(st.selectbox('Fuel:',('Diesel','Petrol','CNG','EV','LPG')))
    seller_type = str(st.selectbox('Seller_Type: ',('Dealer','Individual','TrustmarkDealer')))
    transmission = str(st.selectbox('Transmission: ',('Manual','Automatic')))
    owner = str(st.selectbox('Owner: ',('FirstOwner','SecondOwner','ThirdOwner','Fourth&AboveOwner','TestDriveCar')))
    mileage = int(st.number_input("Mileage (kmpl): "))
    engine = int(st.number_input("Engine: "))
    max_power = int(st.number_input("Max_Power (BHP): "))
    torque = str(st.text_input("Torque (Optional): "))
    seats = int(st.selectbox('No. of Seats: ',(2,4,5,6,7,8)))
    if st.button("Predict"):
        st.write("### Uploading the given data points...")
        if torque is None:
            torque = "NA"
        conn2 = psycopg2.connect(host='35.240.192.226', port=5435, dbname='users', user='postgres', password='ravish')
        with conn2:
            cur = conn2.cursor()
            #st.write(name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,torque,seats)
            cur.execute("insert into car_details(name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,torque,seats) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,torque,seats))
            st.write("#### Computing the best price...")
            q2="select predicted_selling_price::json->'predictions'->0->'value' as predicted_selling_price from (select ml_predict_row('projects/raves-altostrat/locations/asia-southeast1/endpoints/3421627409080778752', json_build_object('instances',json_build_array(json_build_object('name',cd.name,'year',cast(cd.year as VARCHAR),'km_driven',cast(cd.km_driven as VARCHAR),'fuel',cd.fuel,'seller_type',cd.seller_type,'transmission',cd.transmission,'owner',cd.owner,'mileage',cd.mileage,'engine',CAST(cd.engine AS VARCHAR),'max_power',cd.max_power,'torque',cd.torque,'seats',CAST(cd.seats AS VARCHAR))))) as predicted_selling_price from car_details cd where id = (select max(id) from car_details)) as json_query"
            cur.execute(q2)
            psp = cur.fetchone()
            st.write("### Best possible price (INR): ",psp[0])
            predicted_price = psp[0]
            predicted_price = math.floor(predicted_price)
            print(f"Predicted Price: {predicted_price}")
            q3="update car_details set predicted_selling_price = %s where id = (select max(id) from car_details)"
            cur.execute(q3,[predicted_price])
            print(f"Number of rows updated: {cur.rowcount}")
            st.write("Done.")
        cur.close()
        conn2.close()

    else:
        st.write("Get the best price for your car...")

def main():
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("One-stop shop to get the right price for your car.")
    st.markdown('---')
    menu = ["Home","Inventory","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    st.sidebar.info("Click *Home* for Inventory !!")
    st.sidebar.image("power-by-cloud.png",use_column_width=True,clamp=True)
    if choice == "Home":
        sell_car()
    elif choice =="Inventory":
        inventory()
    elif choice =="About":
        i=0
        for i in range(12):
            st.write("")
        st.markdown('## <p style=''font-size:150%;text-align:center;''> Following DEMO is developed and managed by <u>Google Cloud Platform Customer Engineer Team</u> !! </p>',unsafe_allow_html=True)
        st.markdown('---')
        st.balloons()

main()

