# Energy API Collector
Collects json-data from eon based grids and stores them inside a nextcloud. To save space, the files get daily compromized to a 7z-file

# How to start
## Create a nextcloud account
Host your own nextcloud or use one that is already existing.

## Create folder structure
Create a folder structure where you want to store the html files.
I suggest to use something like `energy_api_collector/data/`.

## Create an app password
You shouldn't use your account password for this app. Follow the instructions on `https://docs.nextcloud.com/server/19/user_manual/session_management.html` to create a new device password.

## Collect Environment Variables
We have to set these variables inside the `docker-compose.yaml` file.
```
NEXTCLOUD_URL="https://your.nextcloud.com"
NEXTCLOUD_USER_NAME="your-username"
NEXTCLOUD_PASSWORD="your-app-password"
NEXTCLOUD_BASE_FOLDER="energy_api_collector/data/"
```
Use your base url for `NEXTCLOUD_URL`. Use your username and the new device password you created earlier. 
Use the folder structure from above for `NEXTCLOUD_BASE_FOLDER`.

# Storage
Due to overlapping concerns the script crawls every five minutes, but the data in the api only changes once in 15 minutes.
The json-files have time stamps on their own and the daily compression by the second container guarantees that there is no space wasted.

# Plotting and Display
...
