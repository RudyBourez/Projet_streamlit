import pymongo
import streamlit as st
import pandas as pd
from statistics import mean

client = pymongo.MongoClient(**st.secrets["mongo"])

db = client.Projet
collection_vegetables = db.vegetables
collection_price = db.price

vegetables = [item for item in collection_vegetables.find({}, {"_id":0})]
prices = [item for item in collection_price.find({}, {"_id":0})]

df_vegetables = pd.DataFrame(vegetables)
df_prices = pd.DataFrame(prices)

merged_df = df_vegetables.merge(df_prices, how='inner', on=('Name','Type')) #Fusion des 2 collections
merged_df["Price"] = merged_df["Price"].apply(lambda x : list(map(float, x)))
merged_df["Price €/kg"] = merged_df["Price"].apply(lambda x : mean(x))

bar_chart = df_vegetables.groupby(["Month", "Type"]).count()
st.write(bar_chart)
st.bar_chart(bar_chart.groupby("Month").count())

