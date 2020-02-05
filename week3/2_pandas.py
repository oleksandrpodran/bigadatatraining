import pandas as pd
import numpy as np

data = pd.read_csv(r'C:\sqlite\Automobile_data.csv')

# From given data set print first and last five rows
print(data.head(5))
print(data.tail(5))

# Replace all column values which contain ‘?’ and n.a with NaN.
result = data.replace(['?', 'n.a'], np.nan)
# print(result)

# Print most expensive car’s company name and price.
print(data.loc[data['price'].idxmax(), ['company', 'price']])

# Print All Toyota Cars details
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
data.set_index("company", inplace=True)
print(data.loc[['toyota']])
data.reset_index(inplace=True)

# Count total cars per company
result = data['company'].value_counts()
# print(result)

# Find each company’s Highest price car
result = data[['company', 'price']].groupby(['company']).max()
# print(result)

# Find the average mileage of each car making company
result = data[['company', 'average-mileage']].groupby(['company']).mean()
# print(result)

# Sort all cars by Price column
data.sort_values(by=['price'], ignore_index=True)
# print(data.sort_values(by=['price']))

# Create two data frames using the following two Dicts, Concatenate those two data frames and create a key for each
# data frame: GermanCars = {'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 'Price': [23845, 171995, 135925 ,
# 71400]} japaneseCars = {'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi '], 'Price': [29995, 23600, 61500 ,
# 58900]}
germanCars = pd.DataFrame({'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 'Price': [23845, 171995, 135925, 71400]})
japaneseCars = pd.DataFrame({'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi '], 'Price': [29995, 23600, 61500, 58900]})
frames = [germanCars, japaneseCars]
result = pd.concat(frames, keys=['GermanCars', 'japaneseCars'])
# print(result)
# print(result.loc['GermanCars'])
# print(result.loc['japaneseCars'])

# Create two data frames using the following two Dicts, Merge two data frames, and append second data frame as a new
# column to the first data frame. Car_Price = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'Price': [23845, 17995,
# 135925 , 71400]} car_Horsepower = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'horsepower': [141, 80, 182 , 160]}
car_Price = pd.DataFrame({'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'Price': [23845, 17995, 135925, 71400]})
car_Horsepower = pd.DataFrame({'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'horsepower': [141, 80, 182, 160]})
result = pd.merge(car_Price, car_Horsepower, how='inner', on='Company')
# print(result)
