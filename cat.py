import numpy as np
import re

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
