#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import getvideo
import upload_video as upload_video
import shutil
import os
import subprocess

db = getvideo.Database()

#sql_insert = "INSERT INTO video (title, description, source_id, video_url) VALUES (%s,%s,%s,%s)"
#sql_select = "SELECT * FROM video"

#print(db.query_insert(sql_insert, ['212d','ded','f3ef34','f3f']))


#video = getvideo.get_video()
#video.download_file('http://static.59saniye.com/videos/2018/04/10/20180410155616-6259_1080.mp4', '/var/www/html/GetVideo/video/vid2.mp4')

#a = 'http://static.59saniye.com/videos/2018/04/10/20180410155616-6259_1080.mp4'
#print(a.split('/')[-1])


videos = getvideo.get_video()

last_videos = videos.get_last_uploaded_videos()

for video in last_videos:
	#{'file':'tempvideo/sample.mp4', 'title':'Sample title', 'description':'Description', 'category':'22', 'keywords':'dance,bird', 'privacy':'public'}
	sql_select = "SELECT * FROM video WHERE source_id=%s"
	sql_insert = "INSERT INTO video (title, description, source_id, video_url) VALUES (%s,%s,%s,%s)"

	if not db.query_select(sql_select, video['source_id']):
		db.query_insert(sql_insert, [video['title'], video['description'], video['source_id'],video['video_url']])
		videos.download_file(video['video_url'], '/var/www/html/GetVideo/video/' + video['source_id'] + '.mp4')

		#scale it vith ffmpeg
		subprocess.call('ffmpeg -i /var/www/html/GetVideo/video/{0}.mp4 -c:v libx264 -c:a copy -vf scale=1920:1080,setdar=16/9 /var/www/html/GetVideo/video/{1}.mp4'.format(video['source_id'], video['source_id']+'_scaled'), shell=True)
		#merge the scaled video with the begining video
		subprocess.call('ffmpeg -i /var/www/html/GetVideo/video/{0}.mp4 -i /var/www/html/GetVideo/video/{1}.mp4 -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" /var/www/html/GetVideo/video/{2}.mp4'.format('outputreklam',video['source_id']+'_scaled',video['source_id']+'_merged'), shell=True)
		#Categories: https://gist.github.com/dgp/1b24bf2961521bd75d6c
		#24-> Entertaintment

		upload_video.uploadvideo('/var/www/html/GetVideo/video/'+video['source_id']+'_merged.mp4', video['title'], 'Müneccim şeyi yiyenler: http://banabenianlat.net    '+video['description'], 24, video['title'], 'public')

#Closes open database connections
db.close_db_connection()
#Deletes all files and video download directory
#shutil.rmtree('/var/www/html/GetVideo/video/')
#Creates an empty directory after deleting it
#os.makedirs('/var/www/html/GetVideo/video/', exist_ok=True)
