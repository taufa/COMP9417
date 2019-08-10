
from preprocess import read_data, clean_data

print('-------------------------------------')
print(f'Raw Data.')
print(read_data().describe())
# print(read_data().head())

print('-------------------------------------')
print(f'Cleaned Data.')
print(clean_data().describe())
print(clean_data().head())
