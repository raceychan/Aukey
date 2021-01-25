#Core
import streamlit as st
import streamlit.components.v1 as components

#EDA
import time
import pandas as pd
import numpy as np
import plotly_express as px
from Data_app import Data

class Rank(Data):
###后端    
    @st.cache
    def category_data(category_id): #计算日排名,存入缓存
        data=Rank.rank_load_data(category_id)
        table=data.groupby(['asin','date'])['ranking'].agg('median').apply(lambda x:int(x)).unstack(level=1)
        return table

    def Category_id(category):
        category_id = Rank.catelist[Rank.catelist['category_name']==category]['category_id'].values[0]
        return category_id

    def asin_data(table,chosed_asin):
        asin_raw_rank=pd.DataFrame(table.loc[f'{chosed_asin}',:].dropna()).transpose()
        asin_month_rank=asin_raw_rank.apply(lambda x: int(np.median(x)),axis=1)[0]
        table_chosed_asin=pd.DataFrame(table.loc[f'{chosed_asin}'])
        table_chosed_asin['date']=table_chosed_asin.index.get_level_values(0)
        table_chosed_asin.reset_index(drop=True)
        asin_median_rank=table.apply(lambda x: np.median(x),axis=1).sort_values()
        return table_chosed_asin,asin_month_rank,asin_median_rank

    def linechar(chosed_asin,table_chosed_asin,asin_month_rank):
        fig = px.line(table_chosed_asin, x=table_chosed_asin['date'], y=table_chosed_asin[f'{chosed_asin}'], title=f'{chosed_asin}的当月排名情况(红线为当月排名)')
        fig.add_shape(type='line',
                        x0=table_chosed_asin['date'].iloc[0],
                        y0=asin_month_rank,
                        x1=table_chosed_asin['date'].iloc[-1],
                        y1=asin_month_rank,
                        line=dict(color='Red'),
                        xref='x',
                        yref='y')
        return fig
    
    def table_sort(table,end_time):
        tsort = table[f'{end_time}'].sort_values()
        top1 = tsort[0]
        topn = tsort.where(tsort<=8).count()
        return tsort,top1,topn
###前端
    def run_rank():
        st.title('当月排名进度')
        category_name = st.selectbox('品类名称:',Rank.catelist['category_name'])
        category_id = Rank.Category_id(category_name)
        st.markdown(f'#### 已选中 **{category_name}** ,  品类ID: **{category_id}**')

        table = None
        while table is None:
            data_load_state = st.text('正在加载数据')
            table = Rank.category_data(category_id) #将品类数据存入缓存中，用户查看不同ASIN不需要重新查询品类数据
        st.dataframe(table)
        data_load_state.success('✔️ 数据加载完成')
        time.sleep(1)
        data_load_state.text('')

        chosed_asin = st.selectbox('ASIN',table.index.unique())

        #ASIN
        table_chosed_asin, asin_month_rank, asin_median_rank = Rank.asin_data(table,chosed_asin)

        #画图模块   
        fig = Rank.linechar(chosed_asin,table_chosed_asin,asin_month_rank)
        st.plotly_chart(fig, use_container_width=True) 
        #画图模块
        
        st.info(f'ASIN {chosed_asin}的当月排名为:    {int(asin_month_rank)}')
        
        if int(asin_median_rank[0]) == 1:
            st.success(f'当前品类下月排名最高的ASIN为{asin_median_rank.index[0]},  月排名为: {int(asin_median_rank[0])}')
        elif int(asin_median_rank[0]) <= 8:
            st.info(f'当前品类下月排名最高的ASIN为{asin_median_rank.index[0]},  月排名为: {int(asin_median_rank[0])}')
        else:
            st.warning(f'当前品类下月排名最高的ASIN为{asin_median_rank.index[0]},  月排名为: {int(asin_median_rank[0])}')
        d1,d2=st.beta_columns(2)
        with d1:
            start_time = st.date_input("根据日期查看",table_chosed_asin['date'].iloc[0])
        with d2:
            end_time = st.date_input("结束日期",table_chosed_asin['date'].iloc[-1])

        if str(start_time) in table.columns:
            st.write(table.loc[:,start_time:end_time])
#            t3,top1,topn=Rank.table_sort(table,end_time)
            
#            if top1 == 1:
#                st.success(f'{end_time}日 {t3.index[0]} 的日排名为第一！')
#            elif topn >= 4:
#                st.success('有四个个以上ASIN进入前八！')

        else:
            st.write('数据缺失')
            
        with st.beta_expander('原始数据详情',expanded=False):
            i=st.number_input('输入你想要看到的条数',min_value=1,value=50,step=50)
            detail=table.iloc[:i,:]
            st.write(detail)
            
if __name__=='__main__':
    Rank.run_rank()