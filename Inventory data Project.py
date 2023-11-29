#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import matplotlib.pyplot as plt


# ## import the data sets

# In[15]:



df1 = pd.read_excel(r"C:\Users\singh\Downloads\Inventory Dataset.xlsx")
df2 = pd.read_excel(r"C:\Users\singh\Downloads\New Inventory.xlsx")


# ## Assuming df1 and df2 are your two datasets

# In[16]:



merged_df = pd.merge(df1, df2, on='Item Number', how='inner')


# # Create a date range for future dates on a weekly basis with a gap of 7 days

# In[17]:



future_dates = pd.date_range(start=merged_df['Date'].max(), periods=10, freq='7D')



# # Duplicate the merged_df for each future date

# In[27]:



future_df = pd.concat([merged_df]*len(future_dates), ignore_index=True)


# # Assign the future dates to the duplicated dataframe

# In[29]:



future_df['Future Date'] = sorted(list(future_dates)*len(merged_df))


# # Perform forward-fill to propagate the last known inventory value to future dates for each item

# In[30]:



future_df['Inventory'] = future_df.groupby(['Item Number', 'Future Date'])['Inventory'].fillna(method='ffill')


# # Drop duplicate rows

# In[21]:



future_df = future_df.drop_duplicates(subset=['Item Number', 'Future Date'])


# # Keep only the relevant columns

# In[22]:



result_df = future_df.pivot(index='Item Number', columns='Future Date', values='Inventory').sort_index()


# # Print or use result_df for further analysis

# In[23]:



print(result_df)


# In[24]:


result_df


# # bar chart showing total monthly inventory levels

# In[33]:


# Generate a broader date range for demonstration purposes
merged_df['Date'] = pd.date_range(start='2023-01-01', periods=len(merged_df), freq='D')

# Combine the date information into a new column representing the month
merged_df['Month'] = merged_df['Date'].dt.to_period("M")

# Group the data by month and calculate the total inventory for each month
monthly_inventory = merged_df.groupby('Month')['Inventory'].sum()

# Create a bar chart
plt.figure(figsize=(10, 6))
monthly_inventory.plot(kind='bar', color='skyblue')
plt.title('Total Monthly Inventory Levels')
plt.xlabel('Month')
plt.ylabel('Total Inventory')
plt.xticks(rotation=45)
plt.show()


# In[ ]:





# In[ ]:




