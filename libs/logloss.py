import numpy as np

def logloss(truth, prediction):
    
    #prediction matrix should be a Nx5 matrix, where N is the number of animals
    #each row should contain 5 numbers from 0-1, which is the probability for each class
    #classes: euthanized, adoption, transfered, died, returned to owner
    #(not necessarily in that order, but truth and prediction must be consistent)
    
    #truth matrix can either be a Nx5 matrix, where each entry is either a 0 or a 1,
    #or a Nx1 matrix, where each entry is from 0-4.
    
    truth = np.matrix(truth)
    prediction = np.matrix(prediction)
    
    #normalize prediction
    row_sums = prediction.sum(axis=1)
    prediction = prediction / row_sums
    
    #apply boundaries
    maximum = 1-10**-15
    minimum = 10**-15
    prediction[prediction>maximum] = maximum
    prediction[prediction<minimum] = minimum
    
    if (truth.shape[1]==5):
        truth = truth*[[0],[1],[2],[3],[4]]
    truth = truth.T
    
    N = prediction.shape[0]
    
    predictionForTruthClass = prediction[np.arange(prediction.shape[0]), truth]
    return -np.sum(np.log(predictionForTruthClass))/N
