import pandas as pd

file_name = 'source.csv'
df = pd.read_csv(file_name)

df['Total'] = 0 # add new column

time_series = pd.to_datetime(df['Datetime']).dt.tz_localize(tz='UTC') # initiliase timezone in UTC
time_series = time_series.dt.tz_convert(tz='Asia/Dhaka') # convert to UTC+6 timezone; Dhaka is in this timezone
df['Datetime'] = time_series.dt.strftime('%Y-%m-%dT%H:%M:%S.%f') # convert datetime64 object to string
del time_series

df = df.sort_values(by=['Datetime', 'Name']) # sort according to time.
for i, index_label in enumerate(df.index.tolist()):
    if df.loc[index_label]['Name'] == 'ProductA':
        if df.loc[index_label]['Purity'] == 'Pure':
            ProductA_price = df.loc[index_label]['Price']
        if df.loc[index_label]['Purity'] == 'Impure':
            ProductA_price = 0.75*df.loc[index_label]['Price']
        df.at[index_label, 'Total'] = df.loc[index_label]['Amount']*ProductA_price
    if df.loc[index_label]['Name'] == 'ProductB':
        if df.loc[index_label]['Purity'] == 'Pure':
            ProductB_correspond_ProductA_price = df.iloc[i-1]['Price'] # use integer index not index label
        if df.loc[index_label]['Purity'] == 'Impure':
            ProductB_correspond_ProductA_price = 0.75*df.iloc[i-1]['Price'] # use integer index not index label
        df.at[index_label, 'Total'] = df.loc[index_label]['Amount']*ProductB_correspond_ProductA_price

df = df.sort_index() # sort a/c to index
df['Datetime'] = df['Datetime'].str.slice(0, -3) # to truncate unneccesary zeros
df['Total'] = df['Total'].round(2) # rounding to 2 decimal places


df.to_csv('source_modified.csv', index=False) # export to csv