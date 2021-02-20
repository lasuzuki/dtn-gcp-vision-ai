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
