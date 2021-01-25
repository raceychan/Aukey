#Core
import streamlit as st
import streamlit.components.v1 as components

#Pages
from home_app import Home
from rank_app import Rank
from search_app import Search
from nlp_app import Nlp

st.set_page_config(
    page_title='Aukey 2.0 品类排名看板',
    page_icon=':shark:',
    initial_sidebar_state='expanded'
)

def main():
    menu=['排名进度','语义分析']
    choice = st.sidebar.selectbox('Menu',menu)

    #if choice == '主页':
    #    Home.run_home()
    
    if choice== '排名进度':
        Rank.run_rank()
    
    #elif choice == '合并查询':
    #    Search.run_search()

    elif choice == '语义分析':
        Nlp.run_nlp()

if __name__=='__main__':
    main()

#TO-do
#1.日期格式
#2.可视化优化
#3.表格
#4.ASIN和品类best_seller的超链接
#5.ASIN大写
#6.去掉排名提示
