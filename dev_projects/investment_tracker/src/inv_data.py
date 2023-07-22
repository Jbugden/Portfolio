import boto3
import pandas as pd
import config
from datetime import datetime, timedelta
import yfinance as yf



class get_investment_data:

    def __init__(self) -> None:
        pass

        
    def calculate_stock_return(self,ticker, start_date):
        #returns %return of a given stock from a startdate


        # Get today's date
        end_date = datetime.today().strftime('%Y-%m-%d')

        # Fetch historical data for the stock from start_date till today
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        # Calculate the percentage return
        start_price = stock_data['Close'][0]
        end_price = stock_data['Close'][-1]
        percentage_return = (end_price - start_price) / start_price * 100

        return percentage_return


    def get_performance_table(self,data_dic: dict):
        #Returns a datafram with the returns of portfolio

        performance_table =[]
        current_date = datetime.today()

        #portfolio return variables
        portfolio={
            'Stock': 'Portfolio',
            'Since Purchase' :0,
            '5 Year'  :0,
            '1 Year' :0,
            '6 Month' :0,
            '1 Month' :0,
            '1 Week' :0,
            # '1 Day' :0,
        }

        #Iterate through input and call calculate_stock_return for various dates
        for record in data_dic:

            #Getting stock returns
            since_purchase = self.calculate_stock_return(record['Code']+".AX",datetime.strptime(record['Purchase Date'],"%d/%m/%Y").date())
            five_year = self.calculate_stock_return(record['Code']+".AX",current_date - timedelta(days=365 * 5))
            one_year = self.calculate_stock_return(record['Code']+".AX",current_date - timedelta(days=365 * 1))
            six_month = self.calculate_stock_return(record['Code']+".AX",current_date - timedelta(days=365/2))
            one_month  = self.calculate_stock_return(record['Code']+".AX",current_date - timedelta(days=365/12))
            one_week = self.calculate_stock_return(record['Code']+".AX",current_date - timedelta(days=365/52))
            # one_day = self.calculate_stock_return(record['Code']+".AX",current_date - timedelta(days=1))


            #getting individual stock returns
            temp_record ={}
            temp_record['Stock'] = record['Code']
            temp_record['Since Purchase'] = since_purchase
            temp_record['5 Year'] = five_year
            temp_record['1 Year'] = one_year
            temp_record['6 Month'] = six_month
            temp_record['1 Month'] = one_month
            temp_record['1 Week'] = one_week
            # temp_record['1 Day'] = one_day

            portfolio['Since Purchase'] += (since_purchase*record['weight'])
            portfolio['5 Year']  += (five_year*record['weight'])
            portfolio['1 Year'] += (one_year*record['weight'])
            portfolio['6 Month'] += (six_month*record['weight'])
            portfolio['1 Month'] += (one_month*record['weight'])
            portfolio['1 Week'] += (one_week*record['weight'])
            # portfolio['1 Day'] += (one_day*record['weight'])

            performance_table.append(temp_record)

        performance_table.append(portfolio)

        #transform to data frame
        df = pd.DataFrame(performance_table)

        # dataframe_to_image.convert(df,visualisation_library='matplotlib')
        return df

    def get_data(self):


        client = boto3.client(
            's3',
            aws_access_key_id = config.aws_access_key,
            aws_secret_access_key = config.aws_secret_key,
            region_name = 'ap-southeast-2'
        )
        
        # Fetch the list of existing buckets
        clientResponse = client.list_buckets()


        # Print the bucket names one by one
        print('Printing bucket names...')
        for bucket in clientResponse['Buckets']:
            print(f'Bucket Name: {bucket["Name"]}')


        # Create the S3 object
        obj = client.get_object(
            Bucket = 'jbinvestmentdata',
            Key = 'Holdings.csv'
        )

        # Read data from the S3 object
        data = pd.read_csv(obj['Body'])

        #get weight for each stock
        data['weight'] = data['Avail Units'].div(data['Avail Units'].sum())


        data_dic = data[['Code','Avail Units','Purchase $','Purchase Date','weight']].to_dict('records')


        return self.get_performance_table(data_dic)
    
    def get_market_data(self):

        current_date = datetime.today()
        inception_date = datetime.strptime('02/05/2023',"%d/%m/%Y").date()
       
        #Getting market stock returns
        since_purchase = self.calculate_stock_return("^AXJO",inception_date)
        five_year = self.calculate_stock_return("^AXJO",current_date - timedelta(days=365 * 5))
        one_year = self.calculate_stock_return("^AXJO",current_date - timedelta(days=365 * 1))
        six_month = self.calculate_stock_return("^AXJO",current_date - timedelta(days=365/2))
        one_month  = self.calculate_stock_return("^AXJO",current_date - timedelta(days=365/12))
        one_week = self.calculate_stock_return("^AXJO",current_date - timedelta(days=365/52))

        mkt_table =[]
        temp_record ={}
        temp_record['Market Index'] = 'ASX200'
        temp_record['Since Purchase'] = since_purchase
        temp_record['5 Year'] = five_year
        temp_record['1 Year'] = one_year
        temp_record['6 Month'] = six_month
        temp_record['1 Month'] = one_month
        temp_record['1 Week'] = one_week

        mkt_table.append(temp_record)

        df = pd.DataFrame(mkt_table)

        return df



