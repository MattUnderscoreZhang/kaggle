import numpy as np
import re
import pandas as pd
from copy import deepcopy
from datetime import datetime


def percent_outcome(df,outcome_tag):
  """ series should have pandas.DataFrame interface
    return a pandas.Series of probabilities """
  return df.groupby(outcome_tag).apply(lambda x:float(len(x))/len(df))
# end def percent_outcome

def age2day(age):
  """convert age column from year,month,week to day
  use as: df.AgeuponOutcome.apply(age2day)"""

  if type(age) != type("1 year"):
      return np.nan
  # end if
  num_days = {"year":365,"years":365
              ,"month":30,"months":30
              ,"week":7,"weeks":7
              ,"day":1,"days":1}
  num,unit = age.split()
  return int(num)*num_days[unit]
# end def age2day

def sortcol(val,index):
  split = re.split(" |/",val)
  if len(split)-1 < index:
    return np.nan
  else:
    return split[index]

def classify_colors(catdf):
  """ Produce extra columns classifying if each cat has certain attributes."""
  for i in range(4):
    catdf['color_%d'%i] = catdf['Color'].apply(lambda x:sortcol(x,i))

  colors = set(catdf['color_0'].drop_duplicates())
  colors = colors.union(catdf['color_1'].drop_duplicates())
  colors = colors.union(catdf['color_2'].drop_duplicates())
  colors = colors.union(catdf['color_3'].drop_duplicates())
  colors = colors.difference(set([np.nan]))

  maingroups = set([
          'Tabby','Point','Tortie','Orange','Tan','Calico','Lynx','Blue',
          'Black','Gray','Agouti','White','Brown','Lilac'
      ])
  for main in maingroups:
      catdf['has_%s'%main] = 0
      catdf.loc[catdf["Color"].apply(lambda x:main in x),'has_%s'%main] = 1
  colors = colors.difference(maingroups)

  # Groups with orange.
  add = set(["Apricot","Flame","Tiger","Buff","Pink","Yellow"])
  for color in add:
      catdf.loc[catdf["Color"].apply(lambda x: color in x),'has_Orange'] = 1
  colors = colors.difference(add)
  # Groups with brown.
  add = set(["Chocolate","Torbie"])
  for color in add:
      catdf.loc[catdf["Color"].apply(lambda x: color in x),'has_Brown'] = 1
  colors = colors.difference(add)
  # Groups with calico.
  add = set(["Tricolor"])
  for color in add:
      catdf.loc[catdf["Color"].apply(lambda x: color in x),'has_Calico'] = 1
  colors = colors.difference(add)
  # Groups with tan.
  add = set(["Cream","Seal"])
  for color in add:
      catdf.loc[catdf["Color"].apply(lambda x: color in x),'has_Tan'] = 1
  colors = colors.difference(add)
  # Groups with gray.
  add = set(["Silver","Smoke"])
  for color in add:
      catdf.loc[catdf["Color"].apply(lambda x: color in x),'has_Gray'] = 1
  colors = colors.difference(add)
  return catdf.drop(['color_0','color_1','color_2','color_3'],axis=1)

def fix_age(x):
    if pd.isnull(x):
        return x
    else:
        split = x.split(" ")
        if "week" in split[-1]:
            return float(split[0])/52.0
        elif "month" in split[-1]:
            return float(split[0])/12.0
        elif "year" in split[-1]:
            return float(split[0])
        
def get_sex(x):
    if x=="Unknown" or pd.isnull(x):
        return "Unknown"
    else:
        return x.split(" ")[1]

def get_neuter_status(x):
    if x=="Unknown" or pd.isnull(x):
        return "Unknown"
    else:
        return x.split(" ")[0]

def isMixed(x):
    if ("mix" in x.lower()) or ("/" in x) or ("mix"):
        return "Mixed"
    else:
        return "Pure"
    
def fixCatBreed(x):
    print "deprecated, please use fix_cat_breed(df) instead"
    if "domestic" in x.lower():
        if "short" in x.lower():
            return "domestic shorthair"
        elif "medium" in x.lower():
            return "domestic mediumhair"
        elif "long" in x.lower():
            return "domestic longhair"
    elif "siamese" in x.lower():
        return "siamese"
    else:
        return "rare"

def fix_cat_breed(df_cat):
    """ make an extra column in database df named "hair_length"
    put in hair length categorization. Usage: 
        df_cat = df[df.AnimalType=='Cat'].copy(deep=True)
        dc.fix_cat_breed(df_cat)
    """
    df_cat["hair_length"] = ""

    hair_types = ["short","medium","long"]

    for hair_type in hair_types:
        selector = (df_cat.Breed.apply(lambda x:hair_type in x.lower())) &\
                   (df_cat.Breed.apply(lambda x:"domestic" in x.lower()))
        df_cat.loc[selector,"hair_length"] = "domestic " + hair_type
    # end for 

    # special case siamese
    hair_type = "siamese"
    selector = df_cat.Breed.apply(lambda x:hair_type in x.lower())
    df_cat.loc[selector,"hair_length"] = hair_type

    # name remaining ones rare
    df_cat.loc[df_cat.hair_length=="","hair_length"] = "rare"

    # !!!! currently edit data fram inplace
# end def fix_cat_breed
    
def massage_df(df):
  newdf = deepcopy(df)
  newdf["age_numeric"] = df.AgeuponOutcome.apply(fix_age)
  newdf["age_numeric_days"] = newdf.age_numeric * 365.
  newdf['neuter_status'] = df.SexuponOutcome.apply(get_neuter_status)
  newdf['sex'] = df.SexuponOutcome.apply(get_sex)
  newdf['mixed'] = df.Breed.apply(isMixed)
  newdf["time_stamp"] = df.DateTime.apply(lambda string_date:
          datetime.strptime(string_date,"%Y-%m-%d %H:%M:%S") )
  newdf = classify_colors(newdf)
  return newdf
