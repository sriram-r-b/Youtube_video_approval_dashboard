# Youtube Video Approval Dashboard

### Forked from Django Video Encoding and Streaming App

This Django application is designed for video Approval by Youtube Channel Owners. This repo is a microservice implementation of two microservices combo. The other microservice being [Youtube Archive Database](https://github.com/sriram-r-b/Youtube-video-archive) . The archive Database service features a nosql db integrated with firestore to provide free storage of 1 gb data per user. Both microservices as a whole provide a complete solution for channels that need to maintain uniqueness within their content/analysis .

This client has a oauth 2 client for the Youtube Archive Database

## [Demo](https://dashboard-private.onrender.com/) 

##  Features

-   Video Encoding: Utilizes FFmpeg to encode videos into HLS format, making them compatible with a wide range of devices and browsers.
-   Video Duration Calculation: Automatically calculates the duration of uploaded videos.
-   Thumbnail Generation: Generates thumbnails for videos to provide a preview.
-   Drive Integration : populate the dashboard with videos for approval from google drive (note: HLS Zip is also expected to be uploaded to gdrive along with the mp4 video and its details as json considering cost constraints)
-   Youtube Integration : Post adding credentials enables one click upload
-   Extensible: Easily extend the functionality to include more video-related features or customization.
-   Render Compatible : Doesnt need a persistent DB . can pull and upload data to a external db (currently integrations provided with youtube video archive microservice).
This enables indefinitely free hosting(as long as involved companies pricing policy soesnt change.) 

## Installation Process
1. Clone Project from github 
2. Create virtualenv
      ```sh
    $ virtualenv venv
    ```
3. Activate Virtualenv
   ```sh
    $ source venv/Scripts/activate
    ```
4. Add project specific information in .env
5. Make migration
    ```sh
    $ python manage.py makemigrations
    ```
6. Migrate
    ```sh
    $ python manage.py migrate
    ```
7. Create Superuser
    ```sh
    $ python manage.py createsuperuser
    ```
8. if you dont have  ssh , persistent storage access (like render) download hls from google drive and add to db - place credentials as required.
Start Server
    ```sh
    $ python manage.py add_hls_file
    ```
    if you  have  ssh , persistent storage access upload video and encode(enable celery similiar to the main repo from which this repo was forked from).
Start Server
    ```sh
    $ python manage.py encode
    ```
9.   Run the server in desired condition ensuring the security measures
Start Server
    ```sh
    $ python manage.py encode
    ```
    
 ## Contributing

Contributions to the Youtube Video Approval Dashboard are welcome! Feel free to open issues, submit pull requests, or provide feedback.


