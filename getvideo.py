import pymysql.cursors
import urllib3
import requests
from bs4 import BeautifulSoup
import re

class Database(object):
	"""docstring for Database"""
	def __init__(self):
		self.connection = pymysql.connect(host='localhost',
	                             user='',
	                             password='',
	                             db='VideoUpload',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
	#sql is sql query (srtring)
	#data is inserted data (array)
	def query_insert(self, sql, data):
		try:
		    with self.connection.cursor() as cursor:
		        # Run the sql command
		        result = cursor.execute(sql, data)

		    # connection is not autocommit by default. So you must commit to save
		    # your changes.
		    self.connection.commit()
		    return result
		finally:
			x=1	    

	def query_select(self, sql, data):
		try:
		    with self.connection.cursor() as cursor:
		        # Run the sql command
		        cursor.execute(sql, data)
		        result = cursor.fetchall()

		    # connection is not autocommit by default. So you must commit to save
		    # your changes.
		    self.connection.commit()
		    return result
		finally:
		    x=1

	def close_db_connection(self):
		self.connection.close()

class get_video(object):
	#file: filepath of your file which you want to download
	#path: exact path(from the beginning) where you want to save your downloaded file

	def __init__(self):
		self.http = urllib3.PoolManager()
		self.chunk_size = 1000;
		self.newest_videos_page = "https://www.59saniye.com/b/en-yeniler/"


	def download_file(self, file, path):
		r = self.http.request('GET', file, preload_content=False)

		with open(path, 'wb') as out:
			while True:
				#read method takes chunk_size parameter
				data = r.read(self.chunk_size)
				if not data:
					break
				out.write(data)

		r.release_conn()	

	def get_last_uploaded_videos(self):
		page = requests.get(self.newest_videos_page)
		soup = BeautifulSoup(page.content, 'html.parser')
		#id sayfaya göre değişir
		new_videos = soup.find(id="en-yeniler").find_all("li")

		videos = new_videos[:]
		for index, new_video in enumerate(new_videos):
			videos[index]["link"] = new_video.find(class_="thumb").find("a")["href"]
			videos[index]["title"] = new_video.find(class_="thumb").find("a")["title"]
			inner_page = requests.get('http:'+videos[index]["link"])
			inner_html = BeautifulSoup(inner_page.content, 'html.parser')
			videos[index]["description"] = inner_html.find(id="info").get_text()
			inner_html_str = str(inner_html)
			result = re.search('"//(.*)0.mp4', inner_html_str)
			videos[index]["video_url"] = "http://" + result.group(1) + "0.mp4"
			videos[index]["source_id"] = videos[index]["video_url"].split('/')[-1]


		return videos

"""
import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())
html = list(soup.children)[2]
print(html)






	
download_file('http://static.59saniye.com/videos/2018/04/10/20180410155616-6259_1080.mp4', '/var/www/html/GetVideo/video/vid1.mp4')
"""
