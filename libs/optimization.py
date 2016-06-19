import numpy as np
import muliprocessing as mp
import scipy as sci

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
      return sci.optimize.fmin(lambda x:func(x,ints),float_guess,disp=False)
    assert len(int_args)>0
    opts = np.array(list(map(use_fmin,int_args)))
  best = opts.argmin()
  print(opts)
  return (opts[best],int_args[best])
