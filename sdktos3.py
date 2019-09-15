#Goal: the goal of this code is to use amazon sdk to upload photos from a folder on my laptop to amazon s3.
#HackMit2019

import boto3
import logging
import requests
from botocore.exceptions import ClientError

bucket_name = 'hackmitagain'
key_name = 'CrisisKey' #nname of the file you want to send (we can name this whatever we want)

s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
#for some reaosn, this code comes back with an error, but it does create the bucket

import tkinter as tk
from tkinter import filedialog

#file selection (opens dialogue box for user to choose file to send to the 
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename() #records file path of the selected file
print(file_path)

#uploading files to the bucket
s3.upload_file(file_path, bucket_name, key_name)


