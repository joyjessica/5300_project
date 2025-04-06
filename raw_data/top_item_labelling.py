import pandas as pd

combined_df = pd.read_csv("menustat_price_merged.csv")
top5_df = pd.read_csv("top_items_data.csv")

#print(top5_df['restaurant'].value_counts())

#print(top5_df[top5_df['restaurant'].str.contains("Chili's")]['popular_item'])

#print(combined_df[combined_df['restaurant_x']=='chilis'][combined_df['item'].str.contains("Crispy")])

#print(combined_df['restaurant_x'].value_counts())

change_indices = [147,169,139,185,157,1121,1146,1143,1119,427,435,1470,1431,1457,1429,566,567,574,690,337,319,366,340,1559,1484,1500,1486,762,765,701,771,783,502,515,511,501,845,852,862,900,981,935,42,52,1290,1243,1281,1240,1398,1088,75,97,81,249,257,299]

labelled_df = combined_df

labelled_df['bestseller'] = labelled_df['Unnamed: 0'].isin(change_indices).astype(int)

ms_changed = labelled_df[labelled_df['bestseller']==1]['ms_index']

labelled_df['ms_matched'] = labelled_df['ms_index'].isin(ms_changed).astype(int)

labelled_df_filtered = labelled_df[((labelled_df['bestseller']==0) & (labelled_df['ms_matched']==1))==False]

print(labelled_df.shape)
print(labelled_df_filtered.shape)

print(len(change_indices))
print(len(ms_changed))

labelled_df_filtered = labelled_df_filtered.drop(columns=['Unnamed: 0','restaurant_y','ms_index','item_name','ms_matched']).rename(columns={'restaurant_x':'restaurant'})

print(labelled_df_filtered.columns)


labelled_df_filtered.to_csv("labelled_data.csv",index=True)
