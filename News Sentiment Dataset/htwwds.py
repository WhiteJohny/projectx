import pandas as pd

df = pd.read_csv("Sentiment_dataset.csv")
df.sentiment = df.sentiment.astype(int)
pd.set_option('display.max_columns', None)
print(df)