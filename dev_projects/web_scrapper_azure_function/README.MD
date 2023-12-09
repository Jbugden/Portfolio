# ⚡Creating an Azure Function to Scrape Medicare Data

I had an interesting problem at work, we required a file from medicare to ingest so it can be transformed and consumed appropriateley.

The file is located on the [MBS downlaod site](https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/downloads) and is posted about every 3 months with the latest changes to government schedule fees and each item numbers group.


This project is the development of an Azure function that will extract this file.

### Requirements

Some of the requirements from my manager were:
- It needs to be on Azure functions and triggered with a HTTP request
- The code needs to check if the file already exists in the data lake and only extract the file if there is a new one
- The code also needs to convert the xml file to a csv and add *"LoadDate* which is the date the file is released to the file.
- The file names need to be named YYYYMMDD for the respecitve month and year the file was released.
- **The datalake is a mock datalake i created under my personal Azure account and has since been deleted**

### Methedology

My approach was simple, firstly i created the *get_latest_file_url* function where i extract the latest month availble by finding the header *Most Recent Files* and extracting the text immediately after it.

With this i am able to construct the URL required to access that month's page where the XML file is.

From here i was able to extract the name of the file and construct the URL that is mapped to the file.


Next i created the *check_latest_file_from_storage* function that returns a boolean value based on if the file exists in our data lake. If a False is returned then i call the *add_file_to_storage* function that extracts the xml and converts it to a csv file then uploads it to a storage account on azure.


