# dtn-gcp-vision-ai
This project has been developed by Dr Lara Suzuki :woman_technologist: [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/larasuzuki.svg?style=social&label=Follow%20%40larasuzuki)](https://twitter.com/larasuzuki) and supervised by Vint Cerf :technologist: [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/vgcerf.svg?style=social&label=Follow%20%40vgcerf)](https://twitter.com/vgcerf), both at Google Inc.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/lasuzuki/StrapDown.js/graphs/commit-activity)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![Profile views](https://gpvc.arturio.dev/lasuzuki)
[![GitHub contributors](https://img.shields.io/github/contributors/Naereen/StrapDown.js.svg)](https://GitHub.com/lasuzuki/StrapDown.js/graphs/contributors/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/lasuzuki)

[![ForTheBadge built-with-science](http://ForTheBadge.com/images/badges/built-with-science.svg)](https://GitHub.com/lasuzuki/)

## Introduction

In this project follow on the repo which covers how to run DTN on Google Cloud using NASA's implementation of the bundle protocol - ION. The repo can be found [here](https://github.com/lasuzuki/dtn-gcp)

In this new tutorial we introduce the use of Google API service for Vision. Cloud Vision API enables developers to understand the content of an image by encapsulating powerful machine learning models in an easy-to-use REST API. It quickly classifies images into thousands of categories (such as, “sailboat”), detects individual objects and faces within images, and reads printed words contained within images. 

We will be using the Google Cloud Vision API to label images received using DTN. For this we will be using a LABEL_DETECTION request. A LABEL_DETECTION request annotates an image with a label (or "tag") that is selected based on the image content. For example, a picture of a barn may produce a label of "barn", "farm", or some other similar annotation.

## Project Setup

On [Google Cloud Console](console.cloud.google.com), select a project, or create a new one. Google Cloud Platform organizes resources into projects. This allows you to collect all the related resources for a single application in one place.

Your project must enable the Vision API to accept requests. In the previous tutorial, at the time of the creation of the VM we requested that you enabled `Allow full access to all Cloud APIs`. As such, Vision API should already be enabled for you.

## Configuring your VM environment

In your VM instance, execute the following command:
````
$ pip3 install --upgrade pip
````

Then, install setup tools:
````
$ sudo pip3 install setuptools==49.6.0
````

Install grpcio using: 
````
$ pip3 install --no-cache-dir --force-reinstall -Iv grpcio==1.29
````

Finally, install google-cloud-vision
````
$ pip3 install -U google-cloud-vision
````

## The python code

The `vision.py` file formats your request information, like the request type and content. Requests to the Vision API are provided as JSON objects. See the Vision API Reference for complete information on the specific structure of such a request [here](https://cloud.google.com/vision/docs/reference/rest). Your JSON request is only sent when you call execute. This pattern allows you to pass around such requests and call execute as needed.

```python
def run_vision():
    import os
    import shutil
    import os.path
    import time
    import io
    from datetime import datetime
    # Imports the Google Cloud client library
    # [START vision_python_migration_import]
    from google.cloud import vision

    os.system('ionstop')
    os.system('ionstart -I host1.rc')
    
    if os.path.exists("testfile1"):
        print("Executing Vision API...")
        now = datetime.now()

        client = vision.ImageAnnotatorClient()
        # [END vision_python_migration_client]

        # The name of the image file to annotate
        file_name = os.path.abspath('testfile1')

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations
        x = len(labels)
        os.system(f"echo Identified '{x}' Labels in the image...")
        print("Sending Labels via DTN...")
        for label in labels:
        #Send the number of image labels to host 2
            os.system(f'echo "{label.description}" | bpsource ipn:2.1')
 
        name = "file" + str(int(datetime.timestamp(now)))
        os.rename('testfile1',name) 
        path =  "/home/larissasuzuki/ion-open-source-4.0.1/dtn/processed/"
    
    else:
        print("\n")
        print("Waiting for file via DTN...")
        value = "bprecvfile ipn:1.1"
        os.system('bprecvfile ipn:1.1 1')
        if os.path.exists("testfile1"):
            print("File Received via DTN...")
    
    time.sleep(10)
    
if __name__ == '__main__':
    run_vision()
```

## The ION Configuration Files

The ION Configuration Files can be found in the repo [dtn-gcp](https://github.com/lasuzuki/dtn-gcp/tree/main/rcfiles). 

## The ION execution

Start ION in both `host 1` and `host 2`. Once ION has started in both servers, execute the following commands:

Server 2
````
$ ionstart -I host2.rc
$ bpsendfile ipn:2.1 ipn:1.1 name_of_image.jpeg
````

Server 1
````
$ ionstart -I host1.rc
$ python3 vision.py
````










