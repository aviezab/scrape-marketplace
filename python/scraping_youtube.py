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
parser = argparse.ArgumentParser(description='Scrapping youtube trending')
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

print('Proccess Scrapping Running\n')

# In[53]:


link = 'https://www.youtube.com/feed/trending'
driver.get(link)


# In[54]:


soup = bs4.BeautifulSoup(driver.page_source,'lxml')
driver.close()
end_time = time.time()
print('Proccess Scrapping Done! with {}\n'.format(end_time-start_time))

print('Procces to extract information!\n')
# In[55]:


all_videos = soup.find_all("ytd-video-renderer",{"class":"style-scope ytd-expanded-shelf-contents-renderer"})


# In[56]:


def parser_yt_trending(post):
    link = post.find('a').get('href')
    image = post.find('img').get('src')
    deskripsi = all_videos[0].find('yt-formatted-string',{'id':'description-text'}).text
    det_video_user = post.find('div',{'id':'meta'})
    judul = det_video_user.find('a').get('title')
    
    video_det = det_video_user.findAll('span',{'class':'style-scope ytd-video-meta-block'})
    viewers = video_det[0].text
    time_upload = video_det[1].text
    
    return {'judul':judul,'link':link, 'image':image,
           'deskripsi':deskripsi.replace('\n','') ,'viewers':viewers,
           'time':time_upload}


# In[57]:


clean_post = []
for post in all_videos:
    clean_post.append(parser_yt_trending(post))


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


