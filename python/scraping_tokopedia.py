#!/usr/bin/env python
# coding: utf-8

# In[60]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
from pprint import pprint
import json
import argparse
import time


# In[2]:

#Parser
parser = argparse.ArgumentParser(description='Scrapping twitter from Acount')
parser.add_argument('--katagori', default='elektronik', help='Katagori barang yang akan discrapping')
parser.add_argument('--save_format', default='txt', help='Tipe data untuk menyimpan hasil crawling')

args = parser.parse_args()

start_time = time.time()

#Initialization method. 
chrome_options = webdriver.ChromeOptions()
# myProxy = '175.106.17.62:47641'
# chrome_options.add_argument('--proxy-server=%s' % myProxy) 
# chrome_options.add_argument('--headless') #for pop up windows
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-setuid-sandbox')


# In[4]:


driver = webdriver.Chrome(options=chrome_options)


# In[52]:


katagori = args.katagori
print('Proccess Scrapping Running\n')

# In[53]:


base_url = 'https://www.tokopedia.com/p/{}'.format(katagori)
driver.get(base_url)


# In[54]:


soup = bs4.BeautifulSoup(driver.page_source,'lxml')
driver.close()
end_time = time.time()
print('Proccess Scrapping Done! with {}\n'.format(end_time-start_time))

print('Procces to extract information!\n')
# In[55]:


allpost = soup.findAll('div',{'class':'css-bk6tzz e1nlzfl3'})


# In[56]:


def parser_post(post):
    disp_star = 0
    star = 0
    
    link = post.find('a').get('href')
    img_src = post.find('img').get('src')
    det_prod = post.find('div',{'class':'css-11s9vse'})
    nama = det_prod.find('span',{'class':'css-1tu1s3r'}).text
    harga = det_prod.find('span',{'class':'css-o5uqvq'}).text
    reputation = det_prod.find('div',{'class':'css-f70okh'})
    try:
        star_disp = reputation.findAll('img')
        for a_start in star_disp:
            if a_start.get('alt') == 'star':
                disp_star = disp_star + 1
        star = reputation.find('span').text.replace('(','')
        star = star.replace(')','')
    except:
        print('No Rating')
        pass
    
    dict_post = {'nama_product':nama, 'link':link,
                'img':img_src, 'harga':harga,
                'reputation':{'disp_star':disp_star, 'n_rating':star}
                }
    return(dict_post)


# In[57]:


clean_post = []
for post in allpost:
    clean_post.append(parser_post(post))


# In[58]:

end_time = time.time()
print('Extracting data Succes {}, saving from file ...\n'.format(end_time-start_time))


# In[67]:


def saving_doc(clean_post,doc='txt'):
    doc = doc.lower()
    if doc == 'txt':
        with open('data_clean.txt', 'w') as f:
            print(clean_post, file=f)
    elif doc == 'json':
        doc = doc.upper()
        with open('data_clean.JSON', 'w') as file:
             file.write(json.dumps(clean_post))
    else:
        print('Unsupported document')      
    print('Document succes saving as dataclean.{}\n'.format(doc))


# In[68]:


saving_doc(clean_post,doc=args.save_format)


# In[ ]:
print('Displaying example result')

pprint(clean_post[0])


