import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from sqlalchemy import create_engine
from datetime import datetime

sql='''
select * from mws_data.project_20_listings
'''

st.title('傲基2.0品类管理规则')

@st.cache
def load_data(sql):
    engine = create_engine('mysql+pymysql://chencheng:iKWz@4*7W55@10.1.1.202:3306')
    data=pd.read_sql(sql,engine)
    data.rename(columns={'snapshotted_at':'date'},inplace=True)
    data['date']=pd.to_datetime(data['date'].dt.date)
    return data

data_load_state = st.text('Loading data...')
data = load_data(sql)
data_load_state.text('')

if st.checkbox('展示原始数据'):
    st.subheader('原始数据')
    st.write(data)

st.header('品类详情')

st.markdown('针对每个asin，日排名规则为：')
st.markdown('''
如果asin的排名在TOP100**以外**，则每日排名取当日排名的最高值
''')
st.markdown(
    '''如果asin的排名在TOP100**以内**，但每个值都不同，则取中位数'''
)




category = st.selectbox('品类选择:',
data['category_id'].unique()
)
table=pd.pivot_table(data[data['category_id']==category],
values=['ranking'],index=['asin'],
columns=['date'],aggfunc={'ranking':max})
st.write(table['ranking'])

chosed_asin = st.selectbox('具体asin',
data[data['category_id']==category].asin.unique()
)
st.write(table['ranking'].loc[f'{chosed_asin}'])

df=table['ranking'].loc[f'{chosed_asin}']
fig=px.scatter(df, x=df.index,y=df)
st.subheader(f'{chosed_asin}排名变化')
st.plotly_chart(fig)


start_time = st.slider(
    '按照具体日期查看',
    value=datetime(2021,1,28),
    format='MM/DD/YY'
)
#table['Change_in_rank']=table['ranking']['2021-01-14']-table['ranking']['2021-01-15']
if start_time in table['ranking'].columns:
    st.write(table['ranking'][f'{start_time}'],
    'and change in data compared to previous date is:',
    )
else:
    st.write('data is not yet available now')


if st.checkbox('详细查询'):
    ci=st.multiselect('品类ID',data['category_id'].unique())

    asin=st.multiselect('ASIN',data[data['category_id'].isin(ci)].asin.unique())

    newdate=st.multiselect('日期',data[(data['category_id'].isin(ci))&(data['asin'].isin(asin))].date.unique())

    newtable=data[(data['category_id'].isin(ci))&
    (data['asin'].isin(asin))&(data['date'].isin(newdate))]

    st.write(newtable)







