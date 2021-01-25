#Core
import streamlit as st
import streamlit.components.v1 as components

#EDA
import pandas as pd
from sqlalchemy import create_engine

class Data():
    catelist=pd.read_csv('files/category__.csv')
    local_engine = create_engine('mysql+pymysql://chencheng:iKWz@4*7W55@10.1.1.202:3306')
    cloud_engine = create_engine('mysql+pymysql://root:aukey@888@139.9.201.134:3306')

    nlp_sql='''select distinct asin from amazon.asin_review'''

    def rank_load_data(category_id):
        rank_sql=f'''
        select category_id,category_name,asin,ranking,snapshotted_at as date
        from mws_data.project_20_listings where category_id='{category_id}'
        '''
        data=pd.read_sql(rank_sql,Data.local_engine) 
        data['date']=pd.to_datetime(pd.to_datetime(data['date']).dt.date)
        return data

    def nlp_asins():
        asins = pd.read_sql(Data.nlp_sql,Data.cloud_engine)        
        return asins

    def nlp_data(chosedasin):
        review_sql=f'''
        select review_star_rating,review_info, right(review_date,17) 
        as review_date from amazon.asin_review 
        where asin='{chosedasin}'
        '''  
        review = pd.read_sql(review_sql,Data.cloud_engine)
        return review