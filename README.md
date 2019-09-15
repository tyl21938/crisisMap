# crisisMap

HackMIT project, runs on AWS S3 and Rekognition

files:
rekognitionTest.py
  detectLabels(photo, bucket): 
    -photo is the string name of the image you want to identify as a flood
    -bucket is the string name of the bucket you want to pull from
    
sdktos3.py
  -allows user to select file to send to S3 (if AWS is configured) using sdk commands
