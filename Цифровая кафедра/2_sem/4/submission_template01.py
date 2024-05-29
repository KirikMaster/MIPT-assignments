import numpy as np
import torch
from torch import nn

def create_model():
    # Linear layer mapping from 784 features, so it should be 784->256->16->10

    model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 16),
    nn.ReLU(),
    nn.Linear(16, 10)
    )
    
    # return model instance (None is just a placeholder)
    
    return model

def count_parameters(model):
    num_param = 0
    for param in model.parameters():
        size = 1
        for dim in range(param.ndim):
            size *= param.shape[dim]
        num_param += size
    # return integer number (None is just a placeholder)
    
    return num_param

    
