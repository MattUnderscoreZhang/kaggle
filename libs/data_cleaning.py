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

def sortcol(val,index):
  split = re.split(" |/",val)
  if len(split)-1 < index:
    return np.nan
  else:
    return split[index]

def fix_cat_breed(df_cat):
    """ make an extra column in database df named "catbreed"
    put in hair length categorization. Usage: 
        df_cat = df[df.AnimalType=='Cat'].copy(deep=True)
        dc.fix_cat_breed(df_cat)
    """
    df_cat["catbreed"] = ""

    hair_types = ["short","medium","long"]

    for hair_type in hair_types:
        selector = (df_cat.Breed.apply(lambda x:hair_type in x.lower())) &\
                   (df_cat.Breed.apply(lambda x:"domestic" in x.lower()))
        df_cat.loc[selector,"catbreed"] = "domestic " + hair_type + "hair"
    # end for 

    # special case siamese
    hair_type = "siamese"
    selector = df_cat.Breed.apply(lambda x:hair_type in x.lower())
    df_cat.loc[selector,"catbreed"] = hair_type

    # name remaining ones rare
    df_cat.loc[df_cat.catbreed=="","catbreed"] = "rare"

    # !!!! currently edit data fram inplace
# end def fix_cat_breed

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

def classify_breedsizes(dogdf):
  """ Produce extra columns classifying if each cat has certain attributes."""
  for i in range(5):
    dogdf['size_%d'%i] = dogdf['Breed'].apply(lambda x:sortcol(x,i))

  sizes = set(dogdf['size_0'].drop_duplicates())
  sizes = sizes.union(dogdf['size_1'].drop_duplicates())
  sizes = sizes.union(dogdf['size_2'].drop_duplicates())
  sizes = sizes.union(dogdf['size_3'].drop_duplicates())
  sizes = sizes.union(dogdf['size_4'].drop_duplicates())
  sizes = sizes.difference(set([np.nan]))


  # Groups that are toy.
  add = set(['Chihuahua'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_toy'] = True
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_toy'] = False
  sizes = sizes.difference(add)
  # Groups that are small.
  add = set(['Dachshund','Miniature Poodle','Rat Terrier','Jack Russell Terrier','Yorkshire Terrier','Miniature Schnauzer','Beagle',
          'Cairn Terrier','Shih Tzu'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_small'] = True
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_small'] = False
  sizes = sizes.difference(add)
  # Groups that are medium.
  add = set(['Border Collie','Pit Bull', 'Australian Cattle Dog', 'Australian Kelpie','Staffordshire','Schnauzer'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_medium'] = True
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_medium'] = False
  sizes = sizes.difference(add)
  #Groups that are large.
  add = set(['Australian Shepherd','Catahoula', 'Siberian Husky', 'Pointer'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_large'] = True
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_large'] = False
  sizes = sizes.difference(add)
  # Groups that are extra large.
  add = set(['Labrador Retriever', 'German Shepherd', 'American Staffordshire Terrier'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_xl'] = True
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_xl'] = False
  sizes = sizes.difference(add)
  # Groups that are extra extra large.
  add = set(['Rottweiler','American Bulldog', 'Great Pyrenees'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_xxl'] = True
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_xxl'] = False
  sizes = sizes.difference(add)
  return dogdf.drop(['size_0','size_1','size_2','size_3','size_4'],axis=1)

def massage_df(df):
  newdf = deepcopy(df)
  newdf["age_numeric_days"] = df.AgeuponOutcome.apply(age2day)
  newdf["age_numeric"] = newdf.age_numeric_days / 365.
  newdf['neuter_status'] = df.SexuponOutcome.apply(get_neuter_status)
  newdf['sex'] = df.SexuponOutcome.apply(get_sex)
  newdf['mixed'] = df.Breed.apply(isMixed)
  newdf["time_stamp"] = df.DateTime.apply(lambda string_date:
          datetime.strptime(string_date,"%Y-%m-%d %H:%M:%S") )
  newdf['day_of_week'] = newdf['time_stamp'].apply(lambda x:x.dayofweek)
  newdf['day_of_month'] = newdf['time_stamp'].apply(lambda x:x.day)
  newdf['day_of_year'] = newdf['time_stamp'].apply(lambda x:x.dayofyear)
  newdf['season'] = 0
  newdf.loc[newdf['day_of_year'] >= 79., 'season'] = 1
  newdf.loc[newdf['day_of_year'] >= 171.,'season'] = 2
  newdf.loc[newdf['day_of_year'] >= 265.,'season'] = 3
  newdf.loc[newdf['day_of_year'] >= 355.,'season'] = 0
  newdf['month'] = newdf['time_stamp'].apply(lambda x:x.month)
  newdf = classify_colors(newdf)
  newdf = classify_breedsizes(newdf)
  return newdf
