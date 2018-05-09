import numpy as np
import chrome_trex_api


###### PART 1: PREPARE FIXED VARs AND FUNCTIONs ######
######################################################
######################################################


def relu(array):
    return np.maximum(array, 0.)

def sigmoid(z):
    """
    Compute the sigmoid of z

    Arguments:
    x -- A scalar or numpy array of any size.

    Return:
    s -- sigmoid(z)
    """
    s = 1 / (1 + np.exp(-z))
    return s

def initialize_parameters(n_x, n_h, n_y):
    """
    Argument:
    n_x -- size of the input layer
    n_h -- size of the hidden layer
    n_y -- size of the output layer
    
    Returns:
    params -- python dictionary containing your parameters:
                    W1 -- weight matrix of shape (n_h, n_x)
                    b1 -- bias vector of shape (n_h, 1)
                    W2 -- weight matrix of shape (n_y, n_h)
                    b2 -- bias vector of shape (n_y, 1)
    """
    
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.random.randn(n_h, 1) * 0.5
    W2 = np.random.randn(n_y, n_h) * 1.5
    b2 = np.random.randn(n_y, 1) * 0.15
    
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    
    return parameters


def re_shape_X(X):
    return np.reshape(X, (len(X), 1))

######  PART 2: CREATE A NEURAL NETWORK MODEL   ######
######################################################
######################################################

def tRex_model(X, parameters):
    """
    Argument:
    X -- input data of size (n_x, m)
    parameters -- python dictionary containing your parameters (output of initialization function)
    
    Returns:
    A2 -- The sigmoid output of the second activation
    """
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']

    Z1 = np.dot(W1, X) + b1
    A1 = sigmoid(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = sigmoid(Z2)
    return A2

def from_model_to_action(value, threshold = 0.6):
    if value > threshold:
        chrome_trex_api.press_up()


def wrap_model(X, parameters, n_x):
    X_adj = re_shape_X(X)
    action_value = tRex_model(X_adj, parameters).item()
    # print(action_value)
    from_model_to_action(action_value, threshold = 0.6)


def test_help(X, parameters, n_x):
    X_adj = re_shape_X(X)
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']

    Z1 = np.dot(W1, X_adj) + b1
    A1 = sigmoid(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = sigmoid(Z2)
    print(Z1)
    print(A1)
    print(Z2)
    print(A2)

######      PART 3: RUN AND LOAD THE MODEL      ######
######################################################
######################################################
