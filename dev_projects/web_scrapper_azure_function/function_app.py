import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import dotenv
import os
from azure.storage.filedatalake import  DataLakeServiceClient
import io
import pandas as pd


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# function to return latest available data to download and the file name
def get_latest_file_url():

    # MBS online url
    url ="https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/downloads"

    # get url and check response before proceeding
    response = requests.get(url)

    if response.status_code ==200:
        logging.info('Successfully connected to downloads page')

        # extract html content to find the latest available month to get to the next webpage
        html_content = response.text
        soup= BeautifulSoup(html_content,'html5lib')

        # Finding the heading for "Most Recent Downloads"
        recent_downloads = soup.find('h2', string='Most Recent Files')

        if recent_downloads:
            next_tag = recent_downloads.find_next_sibling()
            latest_month = next_tag.find('a')

            month_text = str(latest_month)

            # extracting name of the of the most recent month available

            start_idx = month_text.find('href="') + len('href="')
            end_idx = month_text.find('"', start_idx)

            page_value =month_text[start_idx:end_idx]

            logging.info(f"Next web page name is {page_value}")

            url =f"https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/{page_value}"

            response = requests.get(url)

            if response.status_code ==200:
                logging.info('Successfully connected to downloads page')

                # extract link for xml download of the most recent month
                html_content = response.text
                soup= BeautifulSoup(html_content,'html5lib')

                file_name = soup.find('u')

                xml =f"https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/219B691F0B58B4C0CA258A4400037AA5/$File/{file_name.text}.XML"

                logging.info(f"Found latest file name {file_name}")

                return file_name.text,xml


            
            else:
                logging.info(f"Bad Request repsonse code on second page: {response.status_code}")
                raise RuntimeError(f"Bad Request repsonse code on second page: {response.status_code}")

        
        else:
            logging.info(f"Could not locate recent downloads element")
            raise RuntimeError(f"Could not locate recent downloads element")


    else:
        logging.info(f"Bad Request repsonse code on first webpage: {response.status_code}")
        raise RuntimeError(f"Bad Request repsonse code on first webpage: {response.status_code}")
        

def check_latest_file_from_storage (incoming_filename: str)-> bool:

    # loading environment variables
    dotenv.load_dotenv()

    account_url = f"https://mydatagen.dfs.core.windows.net"

    sas_token = os.getenv("SAS_TOKEN")

    # conntecting to storage account on azure
    service_client = DataLakeServiceClient(account_url, credential=sas_token)
    # connecting to file system
    file_system_client = service_client.get_file_system_client('filesystem')
    
    # getting paths
    paths = file_system_client.get_paths()
    files =[]
    # only get the files we need based on path and extension
    for path in paths:
        if path.name[-4:] == '.csv' and path.name[:20] == 'mbs_item_number/csv/':
            file_name_with_extension = path.name.rsplit('/', 1)[-1]  
            file_name, file_extension = file_name_with_extension.rsplit('.', 1)
            files.append(file_name)

    files.sort(reverse=True)
    # returns t/f value if file already exists
    if files[0] == incoming_filename[-8:]:
        return True
    else:
        return False

def add_file_to_storage(xml_url :str, file_name :str) -> None:

    response = requests.get(xml_url)

    if response.status_code == 200:
        logging.info('Retrieved File as xml')

        df= pd.read_xml(io.StringIO(response.text))
        df['LoadDate'] = file_name[-8:]

        logging.info('File has been converted to df and load date added')

        csv_data = io.StringIO()
        df.to_csv(csv_data, index=False)

        # reset pointer in memory
        csv_data.seek(0)

        # Connecting to storage

        dotenv.load_dotenv()

        account_url = f"https://mydatagen.dfs.core.windows.net"

        sas_token = os.getenv("SAS_TOKEN")

        # conntecting to storage account on azure
        service_client = DataLakeServiceClient(account_url, credential=sas_token)
        # connecting to file system
        file_system_client = service_client.get_file_system_client('filesystem')

        filepath =f"mbs_item_number/csv/{file_name[-8:]}.csv"

        file_client = file_system_client.get_file_client(filepath)

        file_client.upload_data(csv_data.getvalue(), overwrite=True)
        logging.info('File has been added to storage')



    else:
        logging.info(f"Bad Request repsonse code on xml_retrieval: {response.status_code}")
        raise RuntimeError(f"Bad Request repsonse code on xml_retrieval: {response.status_code}")

@app.route(route="get_mbs_data")
def get_mbs_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file_name,xml =get_latest_file_url()

    if not check_latest_file_from_storage(file_name):
        add_file_to_storage(xml, file_name)

    return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
