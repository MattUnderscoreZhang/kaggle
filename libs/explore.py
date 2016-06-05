import pandas as pd
import numpy as np
import data_cleaning as dc

def load_data(inputfn="data/train.csv",splitfrac=0.6):
  alldf = pd.read_csv(inputfn)
  alldf = dc.massage_df(alldf)
  #alldf = alldf[alldf['AnimalType']=='Cat']

  dc.fix_cat_breed(alldf)

  keep_features = [
      'age_numeric',
      'sex',
      'AnimalType',
      'catbreed',
      'day_of_week',
      'month',
      'neuter_status'
    ]
  colors = [
      'has_Blue', 
      'has_Tortie', 
      'has_White', 
      'has_Brown', 
      'has_Lilac',
      'has_Point', 
      'has_Tabby', 
      'has_Gray', 
      'has_Agouti', 
      'has_Black', 
      'has_Lynx',
      'has_Orange',
      'has_Tan', 
      'has_Calico'
    ]
  sizes = [
    'is_toy',
    'is_small',
    'is_large',
    'is_medium',
    'is_xl',
    'is_xxl'
  ]

  alldf_dummies = pd.get_dummies(alldf[keep_features + colors + sizes].dropna())
  return alldf, alldf_dummies

  # splits data.
  rows = np.random.choice(alldf_dummies.index.values,
      int( round(len(alldf_dummies)*splitfrac) ), replace=False)
  alldf_dummies_train = alldf_dummies.ix[rows]
  alldf_dummies_test = alldf_dummies.drop(rows)
