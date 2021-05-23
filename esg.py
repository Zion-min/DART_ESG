#!/usr/bin/env python
# coding: utf-8

# In[2]:


from urllib.request import urlopen
import bs4
import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import numpy
import numpy as np
import datetime
import  pykrx.stock  as  stock 
import matplotlib.pylab as pylab
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KDTree
from pandas.plotting import scatter_matrix
import datetime


#year -> 2011 ~ 2020
def get_KCGS_ESG(year):
  #url 쿼리 보정
  url = "http://www.cgs.or.kr/business/esg_tab04.jsp?pg=1&sfyear="+str(year)
  html = urlopen(url)
  bs_obj = bs4.BeautifulSoup(html, "html.parser")
  business_board = bs_obj.find("div", {"class":"business_board"})
  url=url+"&pp="+business_board.findAll("tr")[1].find("td").text

  html = urlopen(url)
  bs_obj = bs4.BeautifulSoup(html, "html.parser")
  business_board = bs_obj.find("div", {"class":"business_board"})
  business_board_rows = business_board.findAll("tr")

  column_name_list = []
  column_data_list = []
  for column_name in business_board_rows[0].findAll("th"):
    column_name_list.append(column_name.text)
    column_data_list.append([])

  for row in business_board_rows[1:]:
    for i, elem in enumerate(row.findAll("td")):
      column_data_list[i].append(elem.text)

  m_df=pd.DataFrame()
  column_name_list[2]='기업코드'
  for i, col_name in enumerate(column_name_list):
    m_df[col_name]=column_data_list[i]
  m_df.index=m_df['NO']
  del m_df['NO']
  return m_df

sector_path ='sector.xlsx'
sector = pd.read_excel(sector_path, index_col=0)

esg = {}
for i in range(0,10):
    esg[i] = get_KCGS_ESG(2011 + i)

index = []
for i in range(0,len(sector)):
    index.append(sector.index[i].lstrip('A'))

esg_index = {}
for i in range(0,len(esg)):
    esg_index[i] = []
    for z in range(0,len(esg[i])):
        esg_index[i].append(esg[i]['기업코드'][z])

data = pd.DataFrame({'기업코드':index, '기업명':sector['종목'], '섹터':sector['소분류']})
data.index = data['기업코드']

final_index = {}

for code in range(0,len(esg_index)):
    sil = pd.DataFrame({'기업코드':esg_index[code]})
    sil.index = sil['기업코드']
    sil_index = sil.index

    not_yet = []
    for i in range(0,len(sil_index)):
        if sil_index[i] not in data.index:
            not_yet.append(i)

    final = []
    for i in range(0,len(sil_index)):
        if i not in not_yet:
            final.append(sil_index[i])
    
    sil2 = data.transpose()[final]
    final_index[code] = sil2.transpose()


# In[ ]:




