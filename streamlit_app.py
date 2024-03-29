import streamlit as st
import pandas as pd
import datetime
from datetime import datetime,timedelta,date

st.set_page_config(
    page_title="Labor Planning Model",
    page_icon=":brain:",
    layout="wide"
)

st.title("Labor Planning Model")
st.write("This is a prototype tool is development to compute labor planning requirement based on input parameters")


forecast_template='''business_unit_1,business_unit_2,date,outbound_forecast
wh1,customer1,2024/1/1,1200'''

productivity_template='''business_unit1,business_unit_2,process,unit_rate
wh1,customer1,receiving,250.5
wh1,customer1,putaway,300
wh1,customer1,pick,85
wh1,customer1,pack,100'''

# data input

st.sidebar.header("Please input your data here")
st.sidebar.subheader("Forecasts")
st.sidebar.download_button(label="Click to download a forecast template",data=forecast_template,file_name='forecast_template.csv',mime='text/csv')
forecast_file=st.sidebar.file_uploader("Upload forecast file")

st.sidebar.subheader("Process rates")
st.sidebar.download_button(label="Click to download a rate template file",data=productivity_template,file_name='process_rate_template.csv',mime='text/csv')
rate_file=st.sidebar.file_uploader("Upload process rate file")

if forecast_file is None:
    st.info(" Upload a forecast file through config")
    st.stop()

if rate_file is None:
    st.info(" Upload a process rate file through config")
    st.stop()


df_forecast=pd.read_csv(forecast_file)
df_rate=pd.read_csv(rate_file)

df_forecast['DATE']=pd.to_datetime(df_forecast['DATE']).dt.date

st.subheader("Data view")
col1,col2=st.columns(2)

with col1:
    col1.subheader("Forecast preview")
    st.dataframe(df_forecast)
#col1.line_chart(df_forecast,x='DATE',y='OUTBOUND_FORECAST')

with col2:
    col2.subheader("Process rates")
    st.dataframe(df_rate)


# start the model run

button_result=st.button("Run the model",type="primary")
if button_result==False:
    st.stop()
if button_result==True:
    st.write("Model is running")

def calculate_hours(df1,df2):
    df = df1.merge(df2,on=['BUSINESS_UNIT_1','BUSINESS_UNIT_2'],how='left')
    return df

df_plan=calculate_hours(df_forecast,df_rate)

df_plan['labor_hours']=df_plan['OUTBOUND_FORECAST'] / df_plan['UNIT_RATE']
df_outbound=df_plan[df_plan['PROCESS'].isin(['pick','pack'])]

date_filter=date.today()-timedelta(days=450)

df=df_outbound[df_outbound['DATE']>date_filter]
st.subheader("Daily hours by process")
st.bar_chart(df,x='DATE',y='labor_hours',color='PROCESS')



