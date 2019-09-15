#Goal: the goal of this code is to use amazon sdk to upload photos from a folder on my laptop to amazon s3.
#HackMit2019

import boto3
import logging
import requests
from botocore.exceptions import ClientError
import os


import tkinter as tk
from tkinter import filedialog

def detectLabels(key_name,bucket_name):
    client = boto3.client('rekognition')
##            aws_access_key_id = 'AKIAIJRGEMKGMYNCVEWA',
##            aws_secret_access_key = '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',
##            region_name = "us-east-1",
##            )

    response = client.detect_labels(
        Image = {
            'S3Object': {
                'Bucket': bucket_name,
                'Name': key_name,
            }
        },
        MaxLabels = 5,
        MinConfidence = 80,
    )
    labels = response['Labels']

    for label in labels:
        name = label['Name']
        confidence = label['Confidence']
        #print(label['Name'], label['Confidence'])
        if name == 'Flood':
            print('Flood', confidence)

     return confidence           

def checkingBuckets(s3,bucket_name):
                try:
                                response = s3.head_bucket(Bucket=bucket_name)
                except ClientError as e:
                                logging.debug(e)
                                return False
                return True

def checkingObjects(s3, bucket_name, key_name):
                try:
                                s3.head_object(Bucket=bucket_name, Key=key_name)
                except ClientError as e:
                                logging.debug(e)
                                return False
                return True

def fileUploader(s3, file_path, bucket_name, key_name):
                #uploading files to the bucket
                try:
                                s3.upload_file(file_path, bucket_name, key_name)
                                print('Upload Successful')
                                return True
                except FileNotFoundError:
                                print('File not found. Select another file.')
                                root = tk.Tk()
                                root.withdraw()
                                file_path = filedialog.askopenfilename() #records file path of the selected file
                                print(file_path)
                                
                                fileUploader(file_path, bucket_name, key_name)
##                except NoCredentialsError:
##                                print("Credentials not available'")
##                                return False

def iteratingBuckets(s3, bucket_name):
                #iterating over all keys in the bucket
                paginator = s3.get_paginator('list_objects_v2')
                page_iterator = paginator.paginate(Bucket=bucket_name)

                for page in page_iterator:
                                if page['KeyCount'] > 0:
                                                for item in page['Contents']:
                                                                yield item


def main():
                #function that runs the program
                #goals are to create a bucket (AWS configuration already done), upload a user selected
                #photo to that bucket, and analyze that image using amazon rekognition

                s3 = boto3.client('s3')

                sts_client = boto3.client('sts')

                # Call the assume_role method of the STSConnection object and pass the role
                # ARN and a role session name.
                assumed_role_object=sts_client.assume_role(
                    RoleArn="arn:aws:s3:::crisis-maps-hack-mit",
                    RoleSessionName="AssumeRoleSession1"
                )

                # From the response that contains the assumed role, get the temporary 
                # credentials that can be used to make subsequent API calls
                credentials=assumed_role_object['Credentials']

                # Use the temporary credentials that AssumeRole returns to make a 
                # connection to Amazon S3  
                s3_resource=boto3.resource(
                    's3',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken'],
                )

##                bucket_name = input('enter a new name for the bucket')

                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename() #records file path of the selected file
##                print(file_path)

                base = os.path.basename(file_path)

                key_name = base
                
                #setting nump the logging
                logging.basicConfig(level=logging.DEBUG,
                                    format='%(levelname)s: %(asctime)s: %(message)s')
                #check if the bucket exists
                for bucket in s3_resource.buckets.all():
                                if checkingBuckets(s3,bucket_name):
                                                logging.info(f'{bucket_name} exists and you have permission to accesss.')
                                else:
                                                logging.info(f'{bucket_name} does not exist. it will be created.')
                                                bucket_name = input('name your bucket')
                                                s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
                #check if the key exists
                if checkingObjects(s3, bucket_name, key_name):
                                logging.info('f<key_name} exists.')
                #iterating all keys in the bucket
                                for i in iteratingBuckets(s3, bucket_name):
                                                print(i)
                #creating new key name
                                key_name = input('enter a new name for your key')
                                checkingObjects(s3,bucket_name,key_name)
                else:
##                                logging.info('f<key_name} does not exist. it will be created.')
##                                #file selection (opens dialogue box for user to choose file to send to the 
##                                root = tk.Tk()
##                                root.withdraw()
##                                file_path = filedialog.askopenfilename() #records file path of the selected file
                                print(file_path)
                                
                #upload to the bucket
                if fileUploader(s3,file_path, bucket_name, key_name):
                                 detectLabels(key_name,bucket_name)

                                 #writing condfidence to text file in order to upload to program that will use latitude and longitude of image
                                 outF = open("confidences", "w")
                                for line in confidence:
                                  # write line to output file
                                  outF.write(line)
                                  outF.write("\n")
                                outF.close()
                else:
                                logging.info('f<key_name} was not uploaded.')

                
                                

if __name__ == '__main__':
                main()


