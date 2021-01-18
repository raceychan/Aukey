import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from sqlalchemy import create_engine
from datetime import datetime
st.set_page_config(
    page_title='Aukey 2.0 品类排名看板',
    page_icon=':shark:',
    initial_sidebar_state='expanded'
)


def main():
    menu=['主页','排名','查询','其他']
    choice = st.sidebar.selectbox('工具箱',menu)
    @st.cache
    def load_data():
        data=pd.read_csv('project_20_listings.csv') 
        data.rename(columns={'snapshotted_at':'date'},inplace=True)
        data['date']=pd.to_datetime(pd.to_datetime(data['date']).dt.date)
        return data
    data=load_data()
    if choice == '主页':
        st.title('傲基2.0品类管理')
        st.header('品类详情')
        st.markdown('针对每个asin，日排名规则为：')
        st.markdown('''
        每日排名取当日排名的最高值
        ''')

    elif choice == '排名':
        c1,c2 = st.beta_columns(2)
        category = st.selectbox('CategoryID:',
        data['category_id'].unique()
        )
        table=pd.pivot_table(data[data['category_id']==category],
        values=['ranking'],index=['asin'],
        columns=['date'],aggfunc={'ranking':max})
        st.write(table['ranking'])
        with c1:
            chosed_asin = st.selectbox('Asin',
            data[data['category_id']==category].asin.unique()
            )
            st.write(table['ranking'].loc[f'{chosed_asin}'])
        with c2:

            df=table['ranking'].loc[f'{chosed_asin}']
            fig=px.line(df, x=df.index, y=df, title=f'{chosed_asin}排名变化')
            st.subheader('当月排名变化情况')
            st.plotly_chart(fig)

        start_time = st.slider(
            '该品类下所有Asin的最高日排名',
            value=datetime(2021,1,28),
            format='MM/DD/YY'
        )
        if start_time in table['ranking'].columns:
            st.write(table['ranking'][f'{start_time}'],
            'and change in data compared to previous date is:',
            )
        else:
            st.write('data is not yet available now')

        with st.beta_expander('原始数据详情',expanded=True):
            i=st.number_input('输入你想要看到的条数',min_value=1,value=50,step=50)
            detail=data.iloc[:i,:]
            st.write(detail)


    elif choice == '查询':
        
        ci=st.multiselect('品类ID',data['category_id'].unique())           
        newdate=st.multiselect('日期',data[(data['category_id'].isin(ci))].date.unique())            
        asin=st.multiselect('ASIN',data[data['category_id'].isin(ci)&(data['date'].isin(newdate))].asin.unique())
        newtable=data[(data['category_id'].isin(ci))&(data['asin'].isin(asin))&(data['date'].isin(newdate))]
        st.write(newtable)

if __name__=='__main__':
    main()
