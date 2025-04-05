import pandas as pd
import re

price_df = pd.read_csv("filtered_price_data.csv")
top_df = pd.read_csv("top_items_data.csv")
ms_df = pd.read_csv("menustat_data.csv",low_memory=False)

ms_df['restaurant'] = ms_df['restaurant'].str.replace(" ", "_").str.replace("'", "").str.lower()

#print(price_df[price_df['restaurant']=='mcdonalds'][price_df['item'].str.contains('Chicken McNuggets')].sort_values(by='item')['item'])

#print(ms_df[ms_df['restaurant']=="McDonald's"][ms_df['item_name'].str.contains('Chicken McNuggets')].sort_values(by='item_name')['item_name'])

def get_index(row):

    restaurant = row['restaurant']
    restaurant = restaurant.replace("-","_").lower()

    item = row['item']

    item_words = set(item.lower().replace('(','').replace('(','').replace(',','').split())

    def count_matches(ms_row):
        ms_item = ms_row['item_name']
        row_words = set(ms_item.lower().replace('(','').replace('(','').replace(',','').split())

        if(ms_row['restaurant']!=restaurant):
            return -10
        
        num_match = len(item_words & row_words)

        if((num_match==1) & (ms_item!=item) & (abs(len(row_words)-len(item_words)!=1))):
            return -1
        
        if(num_match == 0):
            return -1

        return num_match

    match_counts = ms_df.apply(count_matches, axis=1)

    if(max(match_counts)==-10):
        return -10

    if(max(match_counts)==-1):
        return -1

    matched_items_length = ms_df[match_counts==max(match_counts)]['item_name'].apply(len)

    return matched_items_length.idxmin()

def is_popular(row):
    return 0

def get_ms_item(index):
    if(index==-1 | index==-10):
        return ""
    else:
        return ms_df.iloc[index]['item_name']

df_combined = pd.DataFrame(
   {
       'restaurant': price_df['restaurant'],
       'item': price_df['item'],
        'ms_index': price_df.apply(get_index,axis=1)
    }
)

ms_df['ms_index'] = ms_df.index

df_combined['ms_item'] = df_combined['ms_index'].apply(lambda i: get_ms_item(i))

df_combined = pd.merge(df_combined, ms_df, on='ms_index')

df_combined.to_csv("menustat_price_merged.csv",index=True)

print(df_combined.head())

print(df_combined.iloc[100:120])