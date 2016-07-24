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

def age_type(age_in_days):
    """ convert age numeric to age type """
    young = 32    # < 1 month
    old   = 5*365 # < 5 years
    if age_in_days < young:
        return "young"
    elif age_in_days < old:
        return "middle"
    else:
        return "old"
    # end if
# end def age_type

def day_of_week_type(day_of_week):
    """ convert day_of_week to weekday/weekends """
    if day_of_week in [5,6]:
        return "weekend"
    else:
        return "weekday"
    # end if
# end def

def is_weekend(dow_type):
    if dow_type == "weekday":
        return 0
    elif dow_type == "weekend":
        return 1
    else:
        print("wtf?!")
    # end if
# end def

def get_sex(x):
    if x=="Unknown" or pd.isnull(x):
        return "Unknown"
    else:
        return x.split(" ")[1]
    # end if
    # return "Male", "Female" or "Unknown"
# end def

def get_neuter_status(x):
    if x=="Unknown" or pd.isnull(x):
        return "Unknown"
    else:
        return x.split(" ")[0]
    # end if
# end def

def just_neuter(status):
    """ decouple neuter status from sex """
    if status in ["Neutered","Spayed"]:
        return "neutered"
    else:
        return status
    # end if
# end def

def isMixed(x):
    if ("mix" in x.lower()) or ("/" in x):
        return "mixed"
    else:
        return "pure"
    # end if
# end def

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
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_toy'] = 1
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_toy'] = 0
  sizes = sizes.difference(add)
  # Groups that are small.
  add = set(['Dachshund','Miniature Poodle','Rat Terrier','Jack Russell Terrier','Yorkshire Terrier','Miniature Schnauzer','Beagle',
          'Cairn Terrier','Shih Tzu'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_small'] = 1
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_small'] = 0
  sizes = sizes.difference(add)
  # Groups that are medium.
  add = set(['Border Collie','Pit Bull', 'Australian Cattle Dog', 'Australian Kelpie','Staffordshire','Schnauzer'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_medium'] = 1
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_medium'] = 0
  sizes = sizes.difference(add)
  #Groups that are large.
  add = set(['Australian Shepherd','Catahoula', 'Siberian Husky', 'Pointer'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_large'] = 1
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_large'] = 0
  sizes = sizes.difference(add)
  # Groups that are extra large.
  add = set(['Labrador Retriever', 'German Shepherd', 'American Staffordshire Terrier'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_xl'] = 1
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_xl'] = 0
  sizes = sizes.difference(add)
  # Groups that are extra extra large.
  add = set(['Rottweiler','American Bulldog', 'Great Pyrenees'])
  for breed in add:
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed in x),'is_xxl'] = 1
      dogdf.loc[dogdf["Breed"].apply(lambda x: breed not in x),'is_xxl'] = False
  sizes = sizes.difference(add)
  return dogdf.drop(['size_0','size_1','size_2','size_3','size_4'],axis=1)
# end def classify_breedsizes

def breed_after_slash(entry):
    if "/" in entry:
        return entry.split("/")[1]
    else:
        return entry.strip(" ")
    # end if
# end def

def dog_breed_info_name(name):
    if "Terr" in name:
        # replace full word, \b defines word boundary
        return re.sub(r'\bTerr\b','',name)
    elif "English Bulldog" in name:
        return "Bulldog"
    elif name == "Anatol Shepherd":
        return "Anatolian Shepherd Dog"
    elif "Yorkshire" in name:
        return "Yorkshire Terrier"
    elif "Pit Bull" in name:
        return "American Pit Bull Terrier"
    elif name == "Wire Hair Fox Terrier":
        return "Wire Fox Terrier"
    elif name == "Chihuahua Shorthair":
        return "Chihuahua"
    elif name == "Dachshund":
        return "Dachshund (Standard)"
    else:
        return name
    # end if
# end def

def dog_breed_akc_name(name):
    # relabel breed names to match those in the American Kennel Club database
    if "English Bulldog" in name:
        return "Bulldog"
    elif name == "Anatol Shepherd":
        return "Anatolian Shepherd"
    elif name == "Standard Poodle":
        return "Poodle"
    elif "Yorkshire" in name:
        return "Yorkshire Terrier"
    elif "Pit Bull" in name:
        return "American Pit Bull Terrier"
    elif name == "Wire Hair Fox Terrier":
        return "Wire Fox Terrier"
    elif name == "Chihuahua Shorthair":
        return "Chihuahua"
    elif "Catahoula" in name:
        return "Catahoula Leopard"
    elif "Staffordshire" in name:
        return "American Staffordshire Terrier"
    elif "Russell" in name:
        return "Russell Terrier"
    elif "Terr" in name:
        # replace full word, \b defines word boundary
        return re.sub(r'\bTerr\b','',name)
    else:
        return name
    # end if
# end def


def massage_df(df):

  newdf = deepcopy(df)

  # animal features 
  # ==== 

  # common to cats and dogs
  # ----
  newdf["age_numeric_days"]  = df.AgeuponOutcome.apply(age2day)
  newdf["age_numeric_years"] = newdf.age_numeric_days / 365.
  newdf["age_numeric"]       = newdf.age_numeric_days / 365. # ! same as years, less descriptive, should be removed
  #newdf['neuter_status']     = df.SexuponOutcome.apply(get_neuter_status)
  newdf["neuter_and_sex"]    = df.SexuponOutcome.apply(get_neuter_status)
  newdf["neuter_status"]     = newdf["neuter_and_sex"].apply(just_neuter)
  newdf['sex']               = df.SexuponOutcome.apply(get_sex)
  newdf['mixed']             = df.Breed.apply(isMixed)
  newdf['has_name']          = df.Name.isnull().apply(lambda x:not x)

  # features specific to cats
  # ----
  newdf = classify_colors(newdf)

  # features specific to dogs
  # ----
  breeds = df.Breed.apply(lambda x:x.replace("Mix",""))
  newdf["dog_breed"] = breeds.apply(breed_after_slash).apply(dog_breed_info_name)
  newdf["akc_name"]  = breeds.apply(breed_after_slash).apply(dog_breed_akc_name)
  newdf["akc_name"]  = newdf["akc_name"].apply(lambda x:x.replace("Dog","").strip())
  
  #newdf = classify_breedsizes(newdf)

  # outcome time related
  # ==== 
  newdf["time_stamp"] = df.DateTime.apply(lambda string_date:
          datetime.strptime(string_date,"%Y-%m-%d %H:%M:%S") )
  newdf['month'] = newdf['time_stamp'].apply(lambda x:x.month)
  newdf['day_of_month'] = newdf['time_stamp'].apply(lambda x:x.day)
  newdf['day_of_year']  = newdf['time_stamp'].apply(lambda x:x.dayofyear)
  newdf['day_of_week']  = newdf['time_stamp'].apply(lambda x:x.dayofweek)

  # classify into weekdays and weekends
  newdf['day_of_week_type'] = newdf.day_of_week.apply(day_of_week_type)
  newdf['is_weekend']       = newdf.day_of_week_type.apply(is_weekend)

  # classify day of year into seasons
  newdf['season'] = "winter" # initialize all to winter, overwrite as needed
  newdf.loc[newdf['day_of_year'] >= 79., 'season'] = "spring"
  newdf.loc[newdf['day_of_year'] >= 171.,'season'] = "summer"
  newdf.loc[newdf['day_of_year'] >= 265.,'season'] = "fall"
  newdf.loc[newdf['day_of_year'] >= 355.,'season'] = "winter"

  return newdf

# end def massage_df

def light_massage(df):

    newdf = deepcopy(df)

    newdf["age_in_days"]    = df.AgeuponOutcome.apply(age2day)
    newdf["neuter_and_sex"] = df.SexuponOutcome.apply(get_neuter_status)
    newdf["neuter_status"]  = newdf["neuter_and_sex"].apply(just_neuter)
    newdf["sex"]            = df.SexuponOutcome.apply(get_sex)
    newdf["mixed"]          = df.Breed.apply(isMixed)
    newdf["has_name"]       = df.Name.isnull().apply(lambda x:not x)

    return newdf
# end def light_massage

