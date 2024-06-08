import numpy as np
from scipy.optimize import minimize
from sklearn.base import BaseEstimator


def entropy(y):  
    """
    Computes entropy of the provided distribution. Use log(value + eps) for numerical stability
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, n_classes)
        One-hot representation of class labels for corresponding subset
    
    Returns
    -------
    float
        Entropy of the provided subset
    """
    EPS = 0.0005
    p = np.sum(y, axis=0) / np.sum(y)
    
    return -np.sum(p * np.log(p + EPS))
    
def gini(y):
    """
    Computes the Gini impurity of the provided distribution
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, n_classes)
        One-hot representation of class labels for corresponding subset
    
    Returns
    -------
    float
        Gini impurity of the provided subset
    """
    p = np.sum(y, axis=0) / np.sum(y)
    
    return 1 - np.sum(np.square(p))
    
def variance(y):
    """
    Computes the variance the provided target values subset
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, 1)
        Target values vector
    
    Returns
    -------
    float
        Variance of the provided target vector
    """
    
    return 1 / y.shape[0] * np.sum(np.square(y - np.mean(y)))

def mad_median(y):
    """
    Computes the mean absolute deviation from the median in the
    provided target values subset
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, 1)
        Target values vector
    
    Returns
    -------
    float
        Mean absolute deviation from the median in the provided vector
    """
    
    return 1 / y.shape[0] * np.sum(np.abs(y - np.median(y)))


def one_hot_encode(n_classes, y):
    y_one_hot = np.zeros((len(y), n_classes), dtype=float)
    y_one_hot[np.arange(len(y)), y.astype(int)[:, 0]] = 1.
    return y_one_hot


def one_hot_decode(y_one_hot):
    return y_one_hot.argmax(axis=1)[:, None]


class Node:
    """
    This class is provided "as is" and it is not mandatory to it use in your code.
    """
    def __init__(self, feature_index, threshold, proba=0):
        self.feature_index = feature_index
        self.value = threshold
        self.proba = proba
        self.type = 'branch' # leaf OR branch
        self.left_child = None
        self.right_child = None
        
        
class DecisionTree(BaseEstimator):
    all_criterions = {
        'gini': (gini, True), # (criterion, classification flag)
        'entropy': (entropy, True),
        'variance': (variance, False),
        'mad_median': (mad_median, False)
    }

    def __init__(self, n_classes=None, max_depth=np.inf, min_samples_split=2, 
                 criterion_name='gini', debug=False):

        assert criterion_name in self.all_criterions.keys(), 'Criterion name must be on of the following: {}'.format(self.all_criterions.keys())
        
        self.n_classes = n_classes
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion_name = criterion_name

        self.depth = 0
        self.root = None # Use the Node class to initialize it later
        self.debug = debug

        
        
    def make_split(self, feature_index, threshold, X_subset, y_subset):
        """
        Makes split of the provided data subset and target values using provided feature and threshold
        
        Parameters
        ----------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels for corresponding subset
        
        Returns
        -------
        (X_left, y_left) : tuple of np.arrays of same type as input X_subset and y_subset
            Part of the providev subset where selected feature x^j < threshold
        (X_right, y_right) : tuple of np.arrays of same type as input X_subset and y_subset
            Part of the providev subset where selected feature x^j >= threshold
        """

        X_left, y_left = X_subset[X_subset[:, feature_index] < threshold, :], y_subset[X_subset[:, feature_index] < threshold]
        X_right, y_right = X_subset[X_subset[:, feature_index] >= threshold, :], y_subset[X_subset[:, feature_index] >= threshold]

        return (X_left, y_left), (X_right, y_right)
    
    def make_split_only_y(self, feature_index, threshold, X_subset, y_subset):
        """
        Split only target values into two subsets with specified feature and threshold
        
        Parameters
        ----------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels for corresponding subset
        
        Returns
        -------
        y_left : np.array of type float with shape (n_objects_left, n_classes) in classification 
                   (n_objects, 1) in regression 
            Part of the provided subset where selected feature x^j < threshold

        y_right : np.array of type float with shape (n_objects_right, n_classes) in classification 
                   (n_objects, 1) in regression 
            Part of the provided subset where selected feature x^j >= threshold
        """
        
        y_left = y_subset[X_subset[:, feature_index] < threshold]
        y_right = y_subset[X_subset[:, feature_index] >= threshold]
        
        return y_left, y_right
    
    def functional(self, threshold : float, feature_index : int, X_subset, y_subset):
        H = self.all_criterions[self.criterion_name][0]
        L, R = self.make_split_only_y(feature_index, threshold, X_subset, y_subset)
        if np.size(L) != 0 and np.size(R) != 0: # No 0-sized subsets
            Q = np.concatenate((L, R), axis=0)
            return -(H(Q) - (len(L) / len(Q) * H(L)) - (len(R) / len(Q) * H(R)))
        else: # L or R is a 0-sized subset
            return 0                 

    def choose_best_split(self, X_subset, y_subset):
        """
        Greedily select the best feature and best threshold w.r.t. selected criterion
        
        Parameters
        ----------
        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels or target values for corresponding subset
        
        Returns
        -------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        """
        
        optimum_candidates = []
        optimum_params = []
        for feature_index in range(X_subset.shape[1]):
            threshold_0 = 0
            optimum = minimize(self.functional, threshold_0, args=(feature_index, X_subset, y_subset), tol=1e-6)
            threshold = optimum.x
            candidate = optimum.fun
            optimum_candidates.append(candidate)
            optimum_params.append((feature_index, threshold))
            
        best_candidate_idx = optimum_candidates.index(min(optimum_candidates))
        (feature_index, threshold) = optimum_params[best_candidate_idx]
        
        return feature_index, threshold
    
    def make_tree(self, X_subset, y_subset):
        """
        Recursively builds the tree
        
        Parameters
        ----------
        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels or target values for corresponding subset
        
        Returns
        -------
        root_node : Node class instance
            Node of the root of the fitted tree
        """

        (feature_index, threshold) = self.choose_best_split(X_subset, y_subset)
        new_node = Node(feature_index, threshold)
        if len(X_subset) >= self.min_samples_split and self.depth <= self.max_depth:
            self.depth += 1
            (X_left, y_left), (X_right, y_right) = self.make_split(feature_index, threshold, X_subset, y_subset)
            if len(y_left) == 0 or len(y_right) == 0:
                new_node.type = 'leaf'
                if self.all_criterions[self.criterion_name][1]: # if classification
                    new_node.value = np.argmax(np.sum(y_subset, axis=0)) # Most frequent
                    new_node.proba = np.sum(y_subset, axis=0) / np.sum(y_subset)
                else: # if regression
                    if self.criterion_name == 'variance':
                        new_node.value = np.mean(y_subset)
                    elif self.criterion_name == 'mad_median':
                        new_node.value = np.median(y_subset)
            else:
                new_node.type = 'branch'
                new_node.left_child = self.make_tree(X_left, y_left)
                new_node.right_child = self.make_tree(X_right, y_right)
            self.depth -= 1
        else:
            new_node.type = 'leaf'
            if self.all_criterions[self.criterion_name][1]: # if classification
                new_node.value = np.argmax(np.sum(y_subset, axis=0)) # Most frequent
                new_node.proba = np.sum(y_subset, axis=0) / np.sum(y_subset)
            else: # if regression
                if self.criterion_name == 'variance':
                    new_node.value = np.mean(y_subset)
                elif self.criterion_name == 'mad_median':
                    new_node.value = np.median(y_subset)
        
        return new_node
        
    def fit(self, X, y):
        """
        Fit the model from scratch using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data to train on

        y : np.array of type int with shape (n_objects, 1) in classification 
                   of type float with shape (n_objects, 1) in regression 
            Column vector of class labels in classification or target values in regression
        
        """
        assert len(y.shape) == 2 and len(y) == len(X), 'Wrong y shape'
        self.criterion, self.classification = self.all_criterions[self.criterion_name]
        if self.classification:
            if self.n_classes is None:
                self.n_classes = len(np.unique(y))
            y = one_hot_encode(self.n_classes, y)

        self.root = self.make_tree(X, y)
    
    def predict(self, X):
        """
        Predict the target value or class label  the model from scratch using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data the predictions should be provided for

        Returns
        -------
        y_predicted : np.array of type int with shape (n_objects, 1) in classification 
                   (n_objects, 1) in regression 
            Column vector of class labels in classification or target values in regression
        
        """
        
        y_predicted = np.zeros((len(X), 1))
        for obj in range(len(X)): 
            current_node = self.root
            x = X[obj, :]
            while True:
                if current_node.type == 'branch':
                    feature_index = current_node.feature_index
                    threshold = current_node.value
                    if x[feature_index] < threshold:
                        current_node = current_node.left_child
                    else:
                        current_node = current_node.right_child
                else:
                    y_predicted[obj] = current_node.value
                    break
        
        return y_predicted
        
    def predict_proba(self, X):
        """
        Only for classification
        Predict the class probabilities using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data the predictions should be provided for

        Returns
        -------
        y_predicted_probs : np.array of type float with shape (n_objects, n_classes)
            Probabilities of each class for the provided objects
        
        """
        assert self.classification, 'Available only for classification problem'

        y_predicted_probs = np.zeros((len(X), self.n_classes))
        for obj in range(len(X)):
            current_node = self.root
            x = X[obj, :]
            while True:
                if current_node.type == 'branch':
                    feature_index = current_node.feature_index
                    threshold = current_node.value
                    if x[feature_index] < threshold:
                        current_node = current_node.left_child
                    else:
                        current_node = current_node.right_child
                else:
                    y_predicted_probs[obj, :] = current_node.proba
                    break
        
        return y_predicted_probs
