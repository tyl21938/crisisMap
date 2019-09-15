% This code prints out confidence scores of whether there is a flood or not when you input an image. 
% Authenticating the IBM Watson Cloud
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    version='{version}', % Version of Visual Recognition
    iam_apikey='{apikey}'% Personal API key from Watson Service or other
)

% Classifying an image
import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='{iam_api_key}')

% An image on your local computer drive (fruitbowl.jpg)
with open('./fruitbowl.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
	classifier_ids='Flooding_1808831974').get_result()
print(json.dumps(classes, indent=2))

