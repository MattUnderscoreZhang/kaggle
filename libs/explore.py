import pandas as pd
import numpy as np
import data_cleaning as dc
import multiprocessing as mp
from scipy.optimize import fmin

def load_data(inputfn="data/train.csv",splitfrac=0.6):
  alldf = pd.read_csv(inputfn)
  alldf = dc.massage_df(alldf)
  alldf = alldf[alldf['AnimalType']=='Cat']

  dc.fix_cat_breed(alldf)

  keep_features = [
      'age_numeric',
      'sex',
      #'AnimalType',
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

  alldf_dummies = pd.get_dummies(alldf[keep_features + colors].dropna())
  return alldf, alldf_dummies

  # splits data.
  rows = np.random.choice(alldf_dummies.index.values,
      int( round(len(alldf_dummies)*splitfrac) ), replace=False)
  alldf_dummies_train = alldf_dummies.ix[rows]
  alldf_dummies_test = alldf_dummies.drop(rows)

def cross_prod(sets):
  mg = np.array(np.meshgrid(*sets))
  mg = mg.swapaxes(0,-1)
  mg = mg.reshape(np.prod(mg.shape[:-1]),mg.shape[-1])
  return mg

def mix_minimizer(func,float_guess=[],int_args=[],nthread=8):
  """ Minimize a function taking a mix of the integer and float inputs.  Floats
  are optimized by scipy, ints by brute force.  Function should be
  func(floats,ints) where floats and ints are iterables. int_args should be a
  list of tuples of integer arguments to check."""

  # Int-only optimization. This is essentially "scipy.brute" but with parallel.
  if len(float_guess)==0:
    assert len(int_args)>0
    with mp.Pool(8) as pool:
      opts = np.array(pool.map(func,int_args))
  else:
    def use_fmin(ints):
      return fmin(lambda x:func(x,ints),float_guess,disp=False)
    assert len(int_args)>0
    opts = np.array(list(map(use_fmin,int_args)))
  best = opts.argmin()
  print(opts)
  return (opts[best],int_args[best])
