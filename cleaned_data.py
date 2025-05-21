import matplotlib as plt
import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd



df = pd.read_csv('/Users/eugenemonama/Downloads/EXCEL/usedcars.csv', names=["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
"drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
"num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
"peak-rpm","city-mpg","highway-mpg","price"])# Reads file and add headers to the columns

df = df.replace('?', pd.NA) #replace ? with NA
print(df.head)
df_cleaned = df.dropna() #drop rows with  NA values
df_cleaned.to_csv('cleaned_file.csv', index=False) #save file to csv
