import boto3
import requests


s3 = boto3.resource('s3',
        aws_access_key_id = input_access_id,
        aws_secret_access_key = input_secret_access_key,
        region_name = "us-east-1",)

#print names of images in bucket
# for bucket in s3.buckets.all():
#     print(bucket.name)


def detectLabels(photo, bucket = 'crisismap'):
    client = boto3.client('rekognition',
            aws_access_key_id = 'AKIAIJRGEMKGMYNCVEWA',
            aws_secret_access_key = '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',
            region_name = "us-east-1",
            )

    response = client.detect_labels(
        Image = {
            'S3Object': {
                'Bucket': bucket,
                'Name': photo,
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


my_bucket = s3.Bucket('crisismap')

for file in my_bucket.objects.all():
    print(file.key)
    detectLabels(file.key)




#TWITTER API
URL = "https://api.twitter.com/1.1/search/tweets.json"
PARAMS = {'q': 'flood', 'lang':'en'}
r = requests.get(url = URL, params=PARAMS)
data = r.json()
print(data)
