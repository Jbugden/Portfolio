import os
# from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from sklearn import preprocessing
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OrdinalEncoder,LabelEncoder,OneHotEncoder

def transform_clean_data(test_data):

    # Identifying missing data

    # 1. Getting null columns
    print("Identifying null columns")
    null_columns = test_data.columns[test_data.isnull().any()]
    null_counts = test_data[null_columns].isnull().sum()

    null_counts_dict = (null_counts/len(test_data)).to_dict()

    col_to_drop =[]

    for k,v in null_counts_dict.items():
        if v > 0.2:
            col_to_drop.append(k)

    test_data = test_data.drop(columns =col_to_drop)
    print("Dropped these columns ", col_to_drop)

    # getting col lis 

    col_list = test_data.columns

    print("Filling NaN Values")

    if 'MSZoning' in col_list:
        test_data['MSZoning'].fillna(test_data['MSZoning'].value_counts().keys().tolist()[0],inplace= True)

    if 'LotFrontage' in col_list:
        test_data['LotFrontage'].fillna(test_data['LotFrontage'].mean(),inplace=True)
    
    if 'Utilities' in col_list:
        test_data['Utilities'].fillna(test_data['Utilities'].value_counts().keys().tolist()[0],inplace= True)

    if 'MasVnrArea' in col_list:
        test_data['MasVnrArea'].fillna(test_data['MasVnrArea'].mean(),inplace=True)

    if 'MasVnrArea' in col_list:
        test_data['BsmtQual'].fillna(test_data['BsmtQual'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtCond' in col_list:
        test_data['BsmtCond'].fillna(test_data['BsmtCond'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'BsmtExposure' in col_list:
        test_data['BsmtExposure'].fillna(test_data['BsmtExposure'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtFinType1' in col_list:
        test_data['BsmtFinType1'].fillna(test_data['BsmtFinType1'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtFinType2' in col_list:
        test_data['BsmtFinType2'].fillna(test_data['BsmtFinType2'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'GarageType' in col_list:
        test_data['GarageType'].fillna(test_data['GarageType'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageFinish' in col_list:
        test_data['GarageFinish'].fillna(test_data['GarageFinish'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageQual' in col_list:
        test_data['GarageQual'].fillna(test_data['GarageQual'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageCond' in col_list:
        test_data['GarageCond'].fillna(test_data['GarageCond'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'GarageYrBlt' in col_list:
        test_data['GarageYrBlt'].fillna(test_data['YearBuilt'],inplace= True)
    
    print("Dropping NaN Rows")
    test_data.dropna(inplace=True)

    # getting Num Cols
    num_col= [
        'LotFrontage'
        ,'LotArea'
        ,'BsmtFinSF1'
        ,'BsmtFinSF2'
        ,'BsmtUnfSF' # basement might be able to be aggregated into one col
        ,'TotalBsmtSF'
        ,'1stFlrSF'
        ,'2ndFlrSF'
        ,'LowQualFinSF'
        ,'GrLivArea'
        ,'BsmtFullBath'
        ,'BsmtHalfBath'
        ,'FullBath'
        ,'HalfBath'
        ,'BedroomAbvGr'
        ,'KitchenAbvGr'
        ,'TotRmsAbvGrd'
        ,'GarageCars'
        ,'GarageArea'
        ,'WoodDeckSF'
        ,'OpenPorchSF'
        ,'EnclosedPorch'
        ,'3SsnPorch'
        ,'ScreenPorch'
        ,'PoolArea'
        ,'MiscVal'
        ,'LotFrontage'
        ,'MasVnrArea'
       

        
        ]

    print("Normalise numerical data")

    num_col = [x for x in num_col if x not in col_to_drop]

    scaler= MinMaxScaler()

    for col in num_col:
    # scaled=scaler.fit_transform(test_data[col].values.reshape(-1, 1))
        test_data[col] =scaler.fit_transform(test_data[[col]])

    ordinal_col =[
    'OverallQual',
    'OverallCond',
    'YearBuilt',
    'YearRemodAdd',
    'ExterQual',
    'ExterCond',
    'BsmtQual',
    'BsmtCond',
    'BsmtExposure',
    'BsmtFinType1',
    'BsmtFinType2',
    'HeatingQC',
    'KitchenQual',
    'FireplaceQu',
    'GarageYrBlt',
    'GarageFinish',
    'GarageQual',
    'GarageCond',
    'PavedDrive',
    'PoolQC',
    'Fence'
    ]

    ordinal_col = [x for x in ordinal_col if x not in col_to_drop]

    cat_col= [
        'MSSubClass'
        ,'MSZoning'
        ,'Street'
        ,'Alley'
        ,'LotShape'
        ,'LandContour'
        ,'Utilities'
        ,'LotConfig'
        ,'LandSlope'
        ,'Neighborhood'
        ,'Condition1'
        ,'Condition2'
        ,'BldgType'
        ,'HouseStyle'
        ,'OverallQual'
        ,'OverallCond'
        ,'RoofStyle'
        ,'RoofMatl'
        ,'MasVnrType'
        ,'ExterQual'
        ,'ExterCond'
        ,'Foundation'
        ,'BsmtQual' #check na condition
        ,'BsmtCond'
        ,'BsmtExposure'
        ,'BsmtFinType1'
        ,'BsmtFinType2'
        ,'Heating'
        ,'HeatingQC'
        ,'CentralAir'
        ,'Electrical'
        ,'KitchenQual'
        ,'Functional'
        ,'FireplaceQu' #- check n/a
        ,'GarageType'
        ,'GarageFinish'
        ,'GarageQual'
        ,'GarageCond'
        ,'PavedDrive'
        ,'PoolQC'
        ,'Fence'
        ,'MiscFeature'
        ,'SaleType'
        ,'SaleCondition'
        ,'Exterior1st'
        ,'Exterior2nd'
        ,'YearBuilt'
        ,'YearRemodAdd'
        ,'GarageYrBlt'
        ,'YrSold'
        ,'MoSold'
       
        ]
    cat_col = [x for x in cat_col if x not in col_to_drop]

    print("encoding categorical data")
    reference_dict={}

    # Processing numerical categories

    # OverallQual
    test_data['OverallQual'] =test_data['OverallQual']/len(test_data['OverallQual'].unique())
    reference_dict['OverallQual'] = [('Very Excellent',1),
                                    ('Excellent',.9),
                                    ('Very Good',.8),
                                    ('Good',.7),
                                    ('Above Average',.6),
                                    ('Average',.5),
                                    ('Below Average',.4),
                                    ('Fair',.3),
                                    ('Poor',.2),
                                    ('Very Poor',.1),
                                    ]


    # OverallCond
    test_data['OverallCond'] =test_data['OverallCond']/len(test_data['OverallCond'].unique())
    reference_dict['OverallCond'] = [('Very Excellent',1),
                                    ('Excellent',.9),
                                    ('Very Good',.8),
                                    ('Good',.7),
                                    ('Above Average',.6),
                                    ('Average',.5),
                                    ('Below Average',.4),
                                    ('Fair',.3),
                                    ('Poor',.2),
                                    ('Very Poor',.1),
                                    ]
    # YearBuilt
    categories =[x for x in test_data['YearBuilt'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['YearBuilt']=enc.fit_transform(test_data[['YearBuilt']])/len(categories)
    reference_dict['YearBuilt'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]


    # 'YearRemodAdd'
    categories =[x for x in test_data['YearRemodAdd'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['YearRemodAdd']=enc.fit_transform(test_data[['YearRemodAdd']])/len(categories)
    reference_dict['YearRemodAdd'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]

    # GarageYrBlt
    categories =[x for x in test_data['GarageYrBlt'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['GarageYrBlt']=enc.fit_transform(test_data[['GarageYrBlt']])/len(categories)
    reference_dict['GarageYrBlt'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]

    # Manual Sorting

    # ExterQual
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['ExterQual'] =x
    for key,val in x:
        test_data['ExterQual']=test_data['ExterQual'].replace(key,val)



    # ExterCond
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['ExterCond'] =x
    for key,val in x:
        test_data['ExterCond']=test_data['ExterCond'].replace(key,val)


    # BsmtQual
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtQual'] =x
    for key,val in x:
        test_data['BsmtQual']=test_data['BsmtQual'].replace(key,val)

    # BsmtCond
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtCond'] =x
    for key,val in x:
        test_data['BsmtCond']=test_data['BsmtCond'].replace(key,val)

    # BsmtExposure
    categories =['NA','No','Mn','Av','Gd']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtExposure'] =x
    for key,val in x:
        test_data['BsmtExposure']=test_data['BsmtExposure'].replace(key,val)


    # BsmtFinType1
    categories =['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtFinType1'] =x
    for key,val in x:
        test_data['BsmtFinType1']=test_data['BsmtFinType1'].replace(key,val)


    # BsmtFinType2
    categories =['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtFinType2'] =x
    for key,val in x:
        test_data['BsmtFinType2']=test_data['BsmtFinType2'].replace(key,val)

    # HeatingQC
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['HeatingQC'] =x
    for key,val in x:
        test_data['HeatingQC']=test_data['HeatingQC'].replace(key,val)


    # KitchenQual
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['KitchenQual'] =x
    for key,val in x:
        test_data['KitchenQual']=test_data['KitchenQual'].replace(key,val)

    # GarageFinish
    categories =['NA','Unf','RFn','Fin']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageFinish'] =x
    for key,val in x:
        test_data['GarageFinish']=test_data['GarageFinish'].replace(key,val)


    # GarageQual
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageQual'] =x
    for key,val in x:
        test_data['GarageQual']=test_data['GarageQual'].replace(key,val)

    # GarageCond
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageCond'] =x
    for key,val in x:
        test_data['GarageCond']=test_data['GarageCond'].replace(key,val)

    # PavedDrive
    categories =['N','P','Y']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['PavedDrive'] =x
    for key,val in x:
        test_data['PavedDrive']=test_data['PavedDrive'].replace(key,val)

    # ordinal_col =[
    #     'OverallQual',
    #     'OverallCond',
    #     'YearBuilt',
    #     'YearRemodAdd',
    #     'ExterQual',
    #     'ExterCond',
    #     'BsmtQual',
    #     'BsmtCond',
    #     'BsmtExposure',
    #     'BsmtFinType1',
    #     'BsmtFinType2',
    #     'HeatingQC',
    #     'KitchenQual',
    #     'FireplaceQu',
    #     'GarageYrBlt',
    #     'GarageFinish',
    #     'GarageQual',
    #     'GarageCond',
    #     'PavedDrive',
    #     'PoolQC',
    #     'Fence'
    #     ]


    cat_col =[x for x in cat_col if x not in list(reference_dict.keys())]

    def label_encoder (col):
        le = LabelEncoder()
        # Transform column
        test_data[col] = le.fit_transform(test_data[col])
        # add encoding to reference dictionary
        reference_dict[col] =[(k,v) for k,v in zip(le.inverse_transform(test_data[col].unique()),test_data[col].unique())]
        for idx,val in enumerate(reference_dict[col]):
            reference_dict[col][idx]=(val[0],val[1]/len(test_data[col].unique()))
        
        # scale the dictionary of values
            
        test_data[col] = test_data[col]/len(test_data[col].unique())
        # scale the dataframe column values

    for col in cat_col:
        label_encoder(col)
    
    print("finished encoding variables and processing data")

    test_data.drop('Id', axis=1, inplace=True)

    return test_data, reference_dict


def transform_clean_data_ohe(test_data):

    # Identifying missing data

    # 1. Getting null columns
    print("Identifying null columns")
    null_columns = test_data.columns[test_data.isnull().any()]
    null_counts = test_data[null_columns].isnull().sum()

    null_counts_dict = (null_counts/len(test_data)).to_dict()

    col_to_drop =[]

    for k,v in null_counts_dict.items():
        if v > 0.2:
            col_to_drop.append(k)

    test_data = test_data.drop(columns =col_to_drop)
    print("Dropped these columns ", col_to_drop)

    # getting col lis 

    col_list = test_data.columns

    print("Filling NaN Values")

    if 'MSZoning' in col_list:
        test_data['MSZoning'].fillna(test_data['MSZoning'].value_counts().keys().tolist()[0],inplace= True)

    if 'LotFrontage' in col_list:
        test_data['LotFrontage'].fillna(test_data['LotFrontage'].mean(),inplace=True)
    
    if 'Utilities' in col_list:
        test_data['Utilities'].fillna(test_data['Utilities'].value_counts().keys().tolist()[0],inplace= True)

    if 'MasVnrArea' in col_list:
        test_data['MasVnrArea'].fillna(test_data['MasVnrArea'].mean(),inplace=True)

    if 'MasVnrArea' in col_list:
        test_data['BsmtQual'].fillna(test_data['BsmtQual'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtCond' in col_list:
        test_data['BsmtCond'].fillna(test_data['BsmtCond'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'BsmtExposure' in col_list:
        test_data['BsmtExposure'].fillna(test_data['BsmtExposure'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtFinType1' in col_list:
        test_data['BsmtFinType1'].fillna(test_data['BsmtFinType1'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtFinType2' in col_list:
        test_data['BsmtFinType2'].fillna(test_data['BsmtFinType2'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'GarageType' in col_list:
        test_data['GarageType'].fillna(test_data['GarageType'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageFinish' in col_list:
        test_data['GarageFinish'].fillna(test_data['GarageFinish'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageQual' in col_list:
        test_data['GarageQual'].fillna(test_data['GarageQual'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageCond' in col_list:
        test_data['GarageCond'].fillna(test_data['GarageCond'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'GarageYrBlt' in col_list:
        test_data['GarageYrBlt'].fillna(test_data['YearBuilt'],inplace= True)
    
    print("Dropping NaN Rows")
    test_data.dropna(inplace=True)

    # getting Num Cols
    num_col= [
        'LotFrontage'
        ,'LotArea'
        ,'BsmtFinSF1'
        ,'BsmtFinSF2'
        ,'BsmtUnfSF' # basement might be able to be aggregated into one col
        ,'TotalBsmtSF'
        ,'1stFlrSF'
        ,'2ndFlrSF'
        ,'LowQualFinSF'
        ,'GrLivArea'
        ,'BsmtFullBath'
        ,'BsmtHalfBath'
        ,'FullBath'
        ,'HalfBath'
        ,'BedroomAbvGr'
        ,'KitchenAbvGr'
        ,'TotRmsAbvGrd'
        ,'GarageCars'
        ,'GarageArea'
        ,'WoodDeckSF'
        ,'OpenPorchSF'
        ,'EnclosedPorch'
        ,'3SsnPorch'
        ,'ScreenPorch'
        ,'PoolArea'
        ,'MiscVal'
        ,'LotFrontage'
        ,'MasVnrArea'
       

        
        ]

    print("Normalise numerical data")

    num_col = [x for x in num_col if x not in col_to_drop]

    scaler= MinMaxScaler()

    for col in num_col:
    # scaled=scaler.fit_transform(test_data[col].values.reshape(-1, 1))
        test_data[col] =scaler.fit_transform(test_data[[col]])

    ordinal_col =[
    'OverallQual',
    'OverallCond',
    'YearBuilt',
    'YearRemodAdd',
    'ExterQual',
    'ExterCond',
    'BsmtQual',
    'BsmtCond',
    'BsmtExposure',
    'BsmtFinType1',
    'BsmtFinType2',
    'HeatingQC',
    'KitchenQual',
    'FireplaceQu',
    'GarageYrBlt',
    'GarageFinish',
    'GarageQual',
    'GarageCond',
    'PavedDrive',
    'PoolQC',
    'Fence'
    ]

    ordinal_col = [x for x in ordinal_col if x not in col_to_drop]

    cat_col= [
        'MSSubClass'
        ,'MSZoning'
        ,'Street'
        ,'Alley'
        ,'LotShape'
        ,'LandContour'
        ,'Utilities'
        ,'LotConfig'
        ,'LandSlope'
        ,'Neighborhood'
        ,'Condition1'
        ,'Condition2'
        ,'BldgType'
        ,'HouseStyle'
        ,'OverallQual'
        ,'OverallCond'
        ,'RoofStyle'
        ,'RoofMatl'
        ,'MasVnrType'
        ,'ExterQual'
        ,'ExterCond'
        ,'Foundation'
        ,'BsmtQual' #check na condition
        ,'BsmtCond'
        ,'BsmtExposure'
        ,'BsmtFinType1'
        ,'BsmtFinType2'
        ,'Heating'
        ,'HeatingQC'
        ,'CentralAir'
        ,'Electrical'
        ,'KitchenQual'
        ,'Functional'
        ,'FireplaceQu' #- check n/a
        ,'GarageType'
        ,'GarageFinish'
        ,'GarageQual'
        ,'GarageCond'
        ,'PavedDrive'
        ,'PoolQC'
        ,'Fence'
        ,'MiscFeature'
        ,'SaleType'
        ,'SaleCondition'
        ,'Exterior1st'
        ,'Exterior2nd'
        ,'YearBuilt'
        ,'YearRemodAdd'
        ,'GarageYrBlt'
        ,'YrSold'
        ,'MoSold'
       
        ]
    cat_col = [x for x in cat_col if x not in col_to_drop]

    print("encoding categorical data")
    reference_dict={}

    # Processing numerical categories

    # OverallQual
    test_data['OverallQual'] =test_data['OverallQual']/len(test_data['OverallQual'].unique())
    reference_dict['OverallQual'] = [('Very Excellent',1),
                                    ('Excellent',.9),
                                    ('Very Good',.8),
                                    ('Good',.7),
                                    ('Above Average',.6),
                                    ('Average',.5),
                                    ('Below Average',.4),
                                    ('Fair',.3),
                                    ('Poor',.2),
                                    ('Very Poor',.1),
                                    ]


    # OverallCond
    test_data['OverallCond'] =test_data['OverallCond']/len(test_data['OverallCond'].unique())
    reference_dict['OverallCond'] = [('Very Excellent',1),
                                    ('Excellent',.9),
                                    ('Very Good',.8),
                                    ('Good',.7),
                                    ('Above Average',.6),
                                    ('Average',.5),
                                    ('Below Average',.4),
                                    ('Fair',.3),
                                    ('Poor',.2),
                                    ('Very Poor',.1),
                                    ]
    # YearBuilt
    categories =[x for x in test_data['YearBuilt'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['YearBuilt']=enc.fit_transform(test_data[['YearBuilt']])/len(categories)
    reference_dict['YearBuilt'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]


    # 'YearRemodAdd'
    categories =[x for x in test_data['YearRemodAdd'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['YearRemodAdd']=enc.fit_transform(test_data[['YearRemodAdd']])/len(categories)
    reference_dict['YearRemodAdd'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]

    # GarageYrBlt
    categories =[x for x in test_data['GarageYrBlt'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['GarageYrBlt']=enc.fit_transform(test_data[['GarageYrBlt']])/len(categories)
    reference_dict['GarageYrBlt'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]

    # Manual Sorting

    # ExterQual
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['ExterQual'] =x
    for key,val in x:
        test_data['ExterQual']=test_data['ExterQual'].replace(key,val)



    # ExterCond
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['ExterCond'] =x
    for key,val in x:
        test_data['ExterCond']=test_data['ExterCond'].replace(key,val)


    # BsmtQual
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtQual'] =x
    for key,val in x:
        test_data['BsmtQual']=test_data['BsmtQual'].replace(key,val)

    # BsmtCond
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtCond'] =x
    for key,val in x:
        test_data['BsmtCond']=test_data['BsmtCond'].replace(key,val)

    # BsmtExposure
    categories =['NA','No','Mn','Av','Gd']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtExposure'] =x
    for key,val in x:
        test_data['BsmtExposure']=test_data['BsmtExposure'].replace(key,val)


    # BsmtFinType1
    categories =['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtFinType1'] =x
    for key,val in x:
        test_data['BsmtFinType1']=test_data['BsmtFinType1'].replace(key,val)


    # BsmtFinType2
    categories =['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtFinType2'] =x
    for key,val in x:
        test_data['BsmtFinType2']=test_data['BsmtFinType2'].replace(key,val)

    # HeatingQC
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['HeatingQC'] =x
    for key,val in x:
        test_data['HeatingQC']=test_data['HeatingQC'].replace(key,val)


    # KitchenQual
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['KitchenQual'] =x
    for key,val in x:
        test_data['KitchenQual']=test_data['KitchenQual'].replace(key,val)

    # GarageFinish
    categories =['NA','Unf','RFn','Fin']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageFinish'] =x
    for key,val in x:
        test_data['GarageFinish']=test_data['GarageFinish'].replace(key,val)


    # GarageQual
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageQual'] =x
    for key,val in x:
        test_data['GarageQual']=test_data['GarageQual'].replace(key,val)

    # GarageCond
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageCond'] =x
    for key,val in x:
        test_data['GarageCond']=test_data['GarageCond'].replace(key,val)

    # PavedDrive
    categories =['N','P','Y']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['PavedDrive'] =x
    for key,val in x:
        test_data['PavedDrive']=test_data['PavedDrive'].replace(key,val)
    
    # ordinal_col =[
    #     'OverallQual',
    #     'OverallCond',
    #     'YearBuilt',
    #     'YearRemodAdd',
    #     'ExterQual',
    #     'ExterCond',
    #     'BsmtQual',
    #     'BsmtCond',
    #     'BsmtExposure',
    #     'BsmtFinType1',
    #     'BsmtFinType2',
    #     'HeatingQC',
    #     'KitchenQual',
    #     'FireplaceQu',
    #     'GarageYrBlt',
    #     'GarageFinish',
    #     'GarageQual',
    #     'GarageCond',
    #     'PavedDrive',
    #     'PoolQC',
    #     'Fence'
    #     ]

    cat_col =[x for x in cat_col if x not in list(reference_dict.keys())]

    for col in cat_col:
        ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform='pandas')
        ohe_df =ohe.fit_transform(test_data[[col]])

        # Remove last column
        remove_col =ohe_df.columns[-1]
        reference_dict[col] = "ohe_"+str(remove_col)
        ohe_df = ohe_df.drop(columns=[remove_col])

        test_data= pd.concat([test_data,ohe_df], axis =1).drop(columns=[col])
    
    print("finished encoding variables and processing data")

    test_data.drop('Id', axis=1, inplace=True)

    return test_data, reference_dict

def transform_clean_data_ohe_prod(test_data):

    # Identifying missing data

    # 1. Getting null columns
    print("Identifying null columns")
    null_columns = test_data.columns[test_data.isnull().any()]
    null_counts = test_data[null_columns].isnull().sum()

    null_counts_dict = (null_counts/len(test_data)).to_dict()

    col_to_drop =[]

    for k,v in null_counts_dict.items():
        if v > 0.2:
            col_to_drop.append(k)

    test_data = test_data.drop(columns =col_to_drop)
    print("Dropped these columns ", col_to_drop)

    # getting col lis 

    col_list = test_data.columns

    print("Filling NaN Values")

    if 'MSZoning' in col_list:
        test_data['MSZoning'].fillna(test_data['MSZoning'].value_counts().keys().tolist()[0],inplace= True)

    if 'LotFrontage' in col_list:
        test_data['LotFrontage'].fillna(test_data['LotFrontage'].mean(),inplace=True)
    
    if 'Utilities' in col_list:
        test_data['Utilities'].fillna(test_data['Utilities'].value_counts().keys().tolist()[0],inplace= True)

    if 'MasVnrArea' in col_list:
        test_data['MasVnrArea'].fillna(test_data['MasVnrArea'].mean(),inplace=True)

    if 'MasVnrArea' in col_list:
        test_data['BsmtQual'].fillna(test_data['BsmtQual'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtCond' in col_list:
        test_data['BsmtCond'].fillna(test_data['BsmtCond'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'BsmtExposure' in col_list:
        test_data['BsmtExposure'].fillna(test_data['BsmtExposure'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtFinType1' in col_list:
        test_data['BsmtFinType1'].fillna(test_data['BsmtFinType1'].value_counts().keys().tolist()[0],inplace= True)

    if 'BsmtFinType2' in col_list:
        test_data['BsmtFinType2'].fillna(test_data['BsmtFinType2'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'GarageType' in col_list:
        test_data['GarageType'].fillna(test_data['GarageType'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageFinish' in col_list:
        test_data['GarageFinish'].fillna(test_data['GarageFinish'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageQual' in col_list:
        test_data['GarageQual'].fillna(test_data['GarageQual'].value_counts().keys().tolist()[0],inplace= True)

    if 'GarageCond' in col_list:
        test_data['GarageCond'].fillna(test_data['GarageCond'].value_counts().keys().tolist()[0],inplace= True)
    
    if 'GarageYrBlt' in col_list:
        test_data['GarageYrBlt'].fillna(test_data['YearBuilt'],inplace= True)
    
    print("Dropping NaN Rows")
    # test_data.dropna(inplace=True)
    columns_with_nan = test_data.columns[test_data.isnull().any()].tolist()

    for column in columns_with_nan:
        most_common_value = test_data[column].mode()[0]  # Calculate the mode
        test_data[column].fillna(most_common_value, inplace=True)

    # getting Num Cols
    num_col= [
        'LotFrontage'
        ,'LotArea'
        ,'BsmtFinSF1'
        ,'BsmtFinSF2'
        ,'BsmtUnfSF' # basement might be able to be aggregated into one col
        ,'TotalBsmtSF'
        ,'1stFlrSF'
        ,'2ndFlrSF'
        ,'LowQualFinSF'
        ,'GrLivArea'
        ,'BsmtFullBath'
        ,'BsmtHalfBath'
        ,'FullBath'
        ,'HalfBath'
        ,'BedroomAbvGr'
        ,'KitchenAbvGr'
        ,'TotRmsAbvGrd'
        ,'GarageCars'
        ,'GarageArea'
        ,'WoodDeckSF'
        ,'OpenPorchSF'
        ,'EnclosedPorch'
        ,'3SsnPorch'
        ,'ScreenPorch'
        ,'PoolArea'
        ,'MiscVal'
        ,'LotFrontage'
        ,'MasVnrArea'
       

        
        ]

    print("Normalise numerical data")

    num_col = [x for x in num_col if x not in col_to_drop]

    scaler= MinMaxScaler()

    for col in num_col:
    # scaled=scaler.fit_transform(test_data[col].values.reshape(-1, 1))
        test_data[col] =scaler.fit_transform(test_data[[col]])

    ordinal_col =[
    'OverallQual',
    'OverallCond',
    'YearBuilt',
    'YearRemodAdd',
    'ExterQual',
    'ExterCond',
    'BsmtQual',
    'BsmtCond',
    'BsmtExposure',
    'BsmtFinType1',
    'BsmtFinType2',
    'HeatingQC',
    'KitchenQual',
    'FireplaceQu',
    'GarageYrBlt',
    'GarageFinish',
    'GarageQual',
    'GarageCond',
    'PavedDrive',
    'PoolQC',
    'Fence'
    ]

    ordinal_col = [x for x in ordinal_col if x not in col_to_drop]

    cat_col= [
        'MSSubClass'
        ,'MSZoning'
        ,'Street'
        ,'Alley'
        ,'LotShape'
        ,'LandContour'
        ,'Utilities'
        ,'LotConfig'
        ,'LandSlope'
        ,'Neighborhood'
        ,'Condition1'
        ,'Condition2'
        ,'BldgType'
        ,'HouseStyle'
        ,'OverallQual'
        ,'OverallCond'
        ,'RoofStyle'
        ,'RoofMatl'
        ,'MasVnrType'
        ,'ExterQual'
        ,'ExterCond'
        ,'Foundation'
        ,'BsmtQual' #check na condition
        ,'BsmtCond'
        ,'BsmtExposure'
        ,'BsmtFinType1'
        ,'BsmtFinType2'
        ,'Heating'
        ,'HeatingQC'
        ,'CentralAir'
        ,'Electrical'
        ,'KitchenQual'
        ,'Functional'
        ,'FireplaceQu' #- check n/a
        ,'GarageType'
        ,'GarageFinish'
        ,'GarageQual'
        ,'GarageCond'
        ,'PavedDrive'
        ,'PoolQC'
        ,'Fence'
        ,'MiscFeature'
        ,'SaleType'
        ,'SaleCondition'
        ,'Exterior1st'
        ,'Exterior2nd'
        ,'YearBuilt'
        ,'YearRemodAdd'
        ,'GarageYrBlt'
        ,'YrSold'
        ,'MoSold'
       
        ]
    cat_col = [x for x in cat_col if x not in col_to_drop]

    print("encoding categorical data")
    reference_dict={}

    # Processing numerical categories

    # OverallQual
    test_data['OverallQual'] =test_data['OverallQual']/len(test_data['OverallQual'].unique())
    reference_dict['OverallQual'] = [('Very Excellent',1),
                                    ('Excellent',.9),
                                    ('Very Good',.8),
                                    ('Good',.7),
                                    ('Above Average',.6),
                                    ('Average',.5),
                                    ('Below Average',.4),
                                    ('Fair',.3),
                                    ('Poor',.2),
                                    ('Very Poor',.1),
                                    ]


    # OverallCond
    test_data['OverallCond'] =test_data['OverallCond']/len(test_data['OverallCond'].unique())
    reference_dict['OverallCond'] = [('Very Excellent',1),
                                    ('Excellent',.9),
                                    ('Very Good',.8),
                                    ('Good',.7),
                                    ('Above Average',.6),
                                    ('Average',.5),
                                    ('Below Average',.4),
                                    ('Fair',.3),
                                    ('Poor',.2),
                                    ('Very Poor',.1),
                                    ]
    # YearBuilt
    categories =[x for x in test_data['YearBuilt'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['YearBuilt']=enc.fit_transform(test_data[['YearBuilt']])/len(categories)
    reference_dict['YearBuilt'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]


    # 'YearRemodAdd'
    categories =[x for x in test_data['YearRemodAdd'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['YearRemodAdd']=enc.fit_transform(test_data[['YearRemodAdd']])/len(categories)
    reference_dict['YearRemodAdd'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]

    # GarageYrBlt
    categories =[x for x in test_data['GarageYrBlt'].unique().tolist()]
    categories.sort()
    enc = OrdinalEncoder(categories=[categories])
    test_data['GarageYrBlt']=enc.fit_transform(test_data[['GarageYrBlt']])/len(categories)
    reference_dict['GarageYrBlt'] = [(key,(val+1)/len(categories)) for val,key in enumerate(categories)]

    # Manual Sorting

    # ExterQual
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['ExterQual'] =x
    for key,val in x:
        test_data['ExterQual']=test_data['ExterQual'].replace(key,val)



    # ExterCond
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['ExterCond'] =x
    for key,val in x:
        test_data['ExterCond']=test_data['ExterCond'].replace(key,val)


    # BsmtQual
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtQual'] =x
    for key,val in x:
        test_data['BsmtQual']=test_data['BsmtQual'].replace(key,val)

    # BsmtCond
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtCond'] =x
    for key,val in x:
        test_data['BsmtCond']=test_data['BsmtCond'].replace(key,val)

    # BsmtExposure
    categories =['NA','No','Mn','Av','Gd']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtExposure'] =x
    for key,val in x:
        test_data['BsmtExposure']=test_data['BsmtExposure'].replace(key,val)


    # BsmtFinType1
    categories =['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtFinType1'] =x
    for key,val in x:
        test_data['BsmtFinType1']=test_data['BsmtFinType1'].replace(key,val)


    # BsmtFinType2
    categories =['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['BsmtFinType2'] =x
    for key,val in x:
        test_data['BsmtFinType2']=test_data['BsmtFinType2'].replace(key,val)

    # HeatingQC
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['HeatingQC'] =x
    for key,val in x:
        test_data['HeatingQC']=test_data['HeatingQC'].replace(key,val)


    # KitchenQual
    categories =['Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['KitchenQual'] =x
    for key,val in x:
        test_data['KitchenQual']=test_data['KitchenQual'].replace(key,val)

    # GarageFinish
    categories =['NA','Unf','RFn','Fin']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageFinish'] =x
    for key,val in x:
        test_data['GarageFinish']=test_data['GarageFinish'].replace(key,val)


    # GarageQual
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageQual'] =x
    for key,val in x:
        test_data['GarageQual']=test_data['GarageQual'].replace(key,val)

    # GarageCond
    categories =['NA','Po','Fa','TA','Gd','Ex']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['GarageCond'] =x
    for key,val in x:
        test_data['GarageCond']=test_data['GarageCond'].replace(key,val)

    # PavedDrive
    categories =['N','P','Y']
    x=[(key,(val+1)/len(categories)) for val,key in enumerate(categories)]
    reference_dict['PavedDrive'] =x
    for key,val in x:
        test_data['PavedDrive']=test_data['PavedDrive'].replace(key,val)
    
    # ordinal_col =[
    #     'OverallQual',
    #     'OverallCond',
    #     'YearBuilt',
    #     'YearRemodAdd',
    #     'ExterQual',
    #     'ExterCond',
    #     'BsmtQual',
    #     'BsmtCond',
    #     'BsmtExposure',
    #     'BsmtFinType1',
    #     'BsmtFinType2',
    #     'HeatingQC',
    #     'KitchenQual',
    #     'FireplaceQu',
    #     'GarageYrBlt',
    #     'GarageFinish',
    #     'GarageQual',
    #     'GarageCond',
    #     'PavedDrive',
    #     'PoolQC',
    #     'Fence'
    #     ]

    cat_col =[x for x in cat_col if x not in list(reference_dict.keys())]

    for col in cat_col:
        ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform='pandas')
        ohe_df =ohe.fit_transform(test_data[[col]])

        # Remove last column
        remove_col =ohe_df.columns[-1]
        reference_dict[col] = "ohe_"+str(remove_col)
        ohe_df = ohe_df.drop(columns=[remove_col])

        test_data= pd.concat([test_data,ohe_df], axis =1).drop(columns=[col])
    
    print("finished encoding variables and processing data")

    test_data.drop('Id', axis=1, inplace=True)

    return test_data, reference_dict
    