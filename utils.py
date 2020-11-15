import numpy as np
import matplotlib.pyplot as plt

def split_train_test(X,y,percent_train=0.9,seed=None):
    if seed!=None:
        np.random.seed(seed)
    ind = np.random.permutation(X.shape[0])
    train = ind[:int(X.shape[0]*percent_train)]
    test = ind[int(X.shape[0]*percent_train):]
    return X[train],X[test], y[train], y[test]    
    
def mse(p,y):
    return np.mean((p-y)**2)
    
def one_hot(y):
    oh = np.zeros((len(y),np.amax(y)+1)) 
    oh[np.arange(len(y)),y]=1
    return oh    
         
def one_hot_to_class(y):
    return np.argmax(y,axis=1)  
  
def accuracy(y_true,y_pred):
    return np.sum(y_true==y_pred)/y_true.shape[0]

def display_probabilities(P):
    fig, ax = plt.subplots(1,10,figsize=(10,1))
    for i in range(10):
        ax[i].imshow(P[i].reshape((28,28)),cmap='gray')
        ax[i].axis('off')    
        
def confusion_matrix(y_true,y_pred):
    cm = np.zeros((np.amax(y_true)+1,np.amax(y_true)+1),dtype=int)
    for i in range(len(y_true)):
        cm[y_true[i],y_pred[i]]+=1
    return cm