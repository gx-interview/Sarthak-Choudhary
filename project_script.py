import pandas as pd

file_name = 'source.csv'
work_file = pd.read_csv(file_name)

# n, m = work_file.shape

df = work_file.sort_values(by=['Datetime', 'Name'])
df['Total'] = 0

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

time_s = pd.to_datetime(df['Datetime']).dt.tz_localize(tz='UTC') # tells pandas that the time is in UTC
time_s = time_s.dt.tz_convert(tz='Asia/Dhaka') # Dhaka is in UTC+6 timezone
df['Datetime'] = time_s.dt.strftime('%Y-%m-%dT%H:%M:%S.%f') # convert datetime64 object to string

df = df.sort_index() 
df['Datetime'] = df['Datetime'].str.slice(0, -3) # to truncate unneccesary zeros

df.to_csv('source_modified.csv', index=False) #export