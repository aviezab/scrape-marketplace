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
parser = argparse.ArgumentParser(description='Scrapping Bukalapak from Catagory')
parser.add_argument('--katagori', default='handphone', help='Katagori barang yang akan discrapping')
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


base_url = 'https://www.bukalapak.com/c/{}/'.format(katagori)
driver.get(base_url)


# In[54]:


soup = bs4.BeautifulSoup(driver.page_source,'lxml')
driver.close()
end_time = time.time()
print('Proccess Scrapping Done! with {}\n'.format(end_time-start_time))

print('Procces to extract information!\n')
# In[55]:


all_produk = soup.find_all("li","product--sem col-12--2")


# In[56]:


def parser_bukalapak(item):
    nama = item.find('a','product__name line-clamp--2 js-tracker-product-link qa-list').get_text()
    harga = item.find("span","amount positive").get_text()
    produk_rating = item.find("span","rating__star js-rating-star")
    try:
        produk_rate = float(produk_rating.text)
    except:
        produk_rate = 0
        
    produk_link = item.find("a").get('href') 
    
    detail_user = item.find('div',{'class':'product-seller'})
    user = detail_user.find('h5',{'class':'user__name'}).text
    user_link = detail_user.find('a').get('href')
    user_city =  detail_user.find('div',{'class':'user-city'}).text
    user_feedback = detail_user.find('a',{'class':'user-feedback-summary'}).text
    user_badge = detail_user.find('div',{'class':'user-level-badge'}).text
    
    dict_hsl = {'nama':nama, 'harga':harga, 'rating_produk':produk_rate,
                'link_produk':produk_link, 'seller':user.replace('\n',''), 
                'seller_link': 'www.bukalapak.com{}'.format(user_link),
                'seller_city': user_city.replace('\n',''), 'seller_feedback': user_feedback,
                'seller_badge': user_badge}
    
    return dict_hsl


# In[57]:


clean_post = []
for item in all_produk:
    clean_post.append(parser_bukalapak(item))

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


