import streamlit as st
import pandas as pd
import time
from Data_app import Data

class Search(Data):

    def run_search():
        st.title('多品类合并查询')
        catelist=pd.read_csv('files/category__.csv')
        category = st.multiselect('品类名称:',catelist['category_name'])
        ci=catelist[catelist['category_name'].isin(category)]['category_id'].apply(lambda x:str(x))  

        st.markdown(f'#### 已选中 **{category}** ,  品类ID: **{ci}**')

        data = None
        while data is None:
            data_load_state=st.text('正在加载数据')
            data=Search.rank_load_data(ci)
        st.write(data)

        ci=catelist[catelist['category_name'].isin(category)]['category_id'].values  
        newdate=st.multiselect('日期',data[(data['category_id'].isin(ci))].date.unique())            
        asin=st.multiselect('ASIN',data[data['category_id'].isin(ci)&(data['date'].isin(newdate))].asin.unique())
        newtable=data[(data['category_id'].isin(ci))&(data['asin'].isin(asin))&(data['date'].isin(newdate))]
        st.write(newtable[['category_id','category_name','asin','ranking','date']])

        data_load_state.success('✔️ 数据加载完成')
        time.sleep(1)
        data_load_state.text('')    
        
if __name__=='__main__':
    Search.run_search()
