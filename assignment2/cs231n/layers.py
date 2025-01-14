from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    out = np.dot(x.reshape(x.shape[0],-1),w)
    out += b
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    dx = np.dot(dout,w.T)
    dx = np.reshape(dx,x.shape)
    dw = np.dot(x.reshape(x.shape[0],-1).T,dout)
    db = np.sum(dout,axis=0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    out = np.maximum(0,x)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    dx = dout
    dx[x <= 0] = 0
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx

##########################################################################################

def leaky_relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    out = np.maximum(0.05*x,x)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def leaky_relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    dx = dout
    dx[x <= 0] *= 0.05
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx

##########################################################################################

def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #############################################################################
        # TODO: [OURS] We have implemented for you the training-time forward pass   #
        # for batch normalization.                                                  #
        # Use minibatch statistics to compute the mean and variance, use these      #
        # statistics to normalize the incoming data, and scale and shift the        #
        # normalized data using gamma and beta.                                     #
        #                                                                           #
        # We need to store the output in the variable out. Any intermediates that   #
        # are needed for the backward pass are stored in the cache variable.        #
        #                                                                           #
        # We use the computed sample mean and variance together with                #
        # the momentum variable to update the running mean and running variance,    #
        # storing the result in the running_mean and running_var variables.         #
        #############################################################################
        
        # sample_mean = np.mean(x,axis=0,keepdims=True)
        # sample_var = np.var(x, axis=0, keepdims=True, ddof=1)
        #
        # x -= sample_mean
        # x /= (np.sqrt(sample_var)+eps)
        #
        # running_mean = momentum * running_mean + (1 - momentum)*sample_mean
        # running_var = momentum * running_var + (1 - momentum) * sample_var
        #
        # x *= gamma
        # x += beta
        #
        # out = x
        
        # FORWARD PASS: Step-by-Step
        
        # Step 1. m = 1 / N \sum x_i
        m = np.mean(x, axis=0, keepdims=True)
        
        # Step 2. xc = x - m
        xc = x - m
        
        # Step 3. xc2 = xc ^ 2
        xcsq = xc ** 2
        
        # Step 4. v = 1 / N \sum xc2_i
        v = np.mean(xcsq, axis=0, keepdims=True)
        
        # Step 5. vsq = sqrt(v + eps)
        vsqrt = np.sqrt(v + eps)
        
        # Step 6. invv = 1 / vsq
        invv = 1.0 / vsqrt
        
        # Step 7. xn = xc * invv
        xn = xc * invv
        
        # Step 8. xg = xn * gamma
        xgamma = xn * gamma
        
        # Step 9. out = xg + beta
        out = xgamma + beta
        
        cache = (x, xc, vsqrt, v, invv, xn, gamma, eps)
        
        running_mean = momentum * running_mean + (1 - momentum) * m
        running_var = momentum * running_var + (1 - momentum) * v
        #######################################################################
        #                           END OF [OUR] CODE                         #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        out  = x - running_mean
        out /= np.sqrt(running_var + eps)
        out *= gamma
        out += beta
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ##############################################################################
    # TODO: [OURS] We have implemented the backward pass for batch normalization.#
    # Results are stored in the dx, dgamma, and dbeta variables.                 #
    ##############################################################################
    (x, xc, vsqrt, v, invv, xn, gamma, eps) = cache
  
    N, D = x.shape
  
    # BACKWARD PASS: Step-byStep
  
    # Step 9. out = xg + beta
    dxg = dout
    dbeta = np.sum(dout, axis=0)
  
    # Step 8. xg = xn * gamma
    dxn = dxg * gamma
    dgamma = np.sum(dxg * xn, axis=0)
  
    # Step 7. xn = xc * invv
    dxc1 = dxn * invv
    dinvv = np.sum(dxn * xc, axis=0)
  
    # Step 6. invv = 1 / vsqrt
    dvsqrt = -1 / (vsqrt ** 2) * dinvv
  
    # Step 5. vsqrt = sqrt(v + eps)
    dv = 0.5 * dvsqrt / np.sqrt(v + eps)
  
    # Step 4. v = 1 / N \sum xcsq_i
    dxcsq = 1.0 / N * np.ones((N, D)) * dv
  
    # Step 3. xcsq = xc ^ 2
    dxc2 = 2.0 * dxcsq * xc
  
    # Step 2. xc = x - m
    dx1 = dxc1 + dxc2
    dm = - np.sum(dxc1 + dxc2, axis=0, keepdims=True)
  
    # Step 1. m = 1 / N \sum x_i
    dx2 = 1.0 / N * np.ones((N, D)) * dm
  
    dx = dx1 + dx2
  
    #############################################################################
    #                             END OF [OUR] CODE                             #
    #############################################################################

    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We drop each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        mask = (np.random.rand(*x.shape) > p) / (1-p)
        out  = x * mask 
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        out = x
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        dx = dout * mask
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == 'test':
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width HH.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    (N,C,H,W)   = x.shape
    (F,_,HH,WW) = w.shape

    stride      = conv_param['stride']
    pad         = conv_param['pad']

    H_prima     = int(1 + (H + 2 * pad - HH) / stride)
    W_prima     = int(1 + (W + 2 * pad - WW) / stride)

    out = np.zeros((N,F,H_prima,W_prima))
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    for n in range(N):
        # Hago el zero padding
        x_pad = np.pad(x[n,:,:,:], ((0,),(pad,),(pad,)), 'constant')
        for f in range(F):
            for h_prima in range(H_prima):
                for w_prima in range(W_prima):
                    # Defino los 4 puntos que determinan la ventana del filtro
                    h1 = h_prima * stride
                    h2 = h_prima * stride + HH
                    w1 = w_prima * stride
                    w2 = w_prima * stride + WW

                    # Le aplico la venta a la entrada
                    ventana = x_pad[:, h1:h2, w1:w2]

                    # Hago la convolución y pongo resultado en out
                    out[n, f, h_prima, w_prima] = np.sum(ventana * w[f,:,:,:]) + b[f]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    (x, w, b, conv_param) = cache

    (N, C, H, W)   = x.shape
    (F, _, HH, WW) = w.shape

    (_, _, H_prima, W_prima) = dout.shape

    stride = conv_param['stride']
    pad = conv_param['pad']

    dx = np.zeros_like(x)
    dw = np.zeros_like(w)
    db = np.zeros_like(b)

    for n in range(N):
        # Hago el zero padding
        dx_pad = np.pad(dx[n,:,:,:], ((0,),(pad,),(pad,)), 'constant')
        x_pad  = np.pad(x[n,:,:,:], ((0,),(pad,),(pad,)), 'constant')
        for f in range(F):
            for h_prima in range(H_prima):
                for w_prima in range(W_prima):
                    # Defino los 4 puntos que determinan la ventana del filtro
                    h1 = h_prima * stride
                    h2 = h_prima * stride + HH
                    w1 = w_prima * stride
                    w2 = w_prima * stride + WW

                    # El gradiente según x es w, por lo que aplico la regla de la cadena
                    # y hago w * dout para el filtro y la venta correspondiente
                    dx_pad[:, h1:h2, w1:w2] += w[f,:,:,:] * dout[n,f,h_prima,w_prima]

                    # El gradiente según w es x, por lo que opero análogo al anterior
                    dw[f,:,:,:] += x_pad[:, h1:h2, w1:w2] * dout[n,f,h_prima,w_prima]

                    # El gradiente según b es 1, por lo que db es igual a dout para
                    # el filtro correspondiente
                    db[f] += dout[n,f,h_prima,w_prima]

        # Le saco el padding a dx
        dx[n,:,:,:] = dx_pad[:,1:-1,1:-1]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    Returns a tuple of:
    - out: Output data
    - cache: (x, pool_param)
    """
    (N,C,H,W) = x.shape

    pool_height = pool_param['pool_height']
    pool_width  = pool_param['pool_width']
    stride      = pool_param['stride']

    # H_out = int(H/pool_height)
    # W_out = int(W/pool_width)

    H_out = int(1 + (H - pool_height) / stride)
    W_out = int(1 + (W - pool_width) / stride)

    out = np.zeros((N,C,H_out,W_out))
    ###########################################################################
    # TODO: Implement the max pooling forward pass                            #
    ###########################################################################
    for n in range(N):
        for h_out in range(H_out):
            for w_out in range(W_out):
                # Defino los 4 puntos que determinan la ventana del filtro
                h1 = h_out * stride
                h2 = h_out * stride + pool_height
                w1 = w_out * stride
                w2 = w_out * stride + pool_width

                # Le aplico la venta a la entrada
                ventana = x[n,:,h1:h2,w1:w2]

                # Me quedo con el máximo de la ventana
                out[n,:,h_out,w_out] = np.max(ventana.reshape((C, pool_height*pool_width)), axis=1)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max pooling backward pass                           #
    ###########################################################################
    
    (x, pool_param) = cache
    (N, C, H, W)    = x.shape

    pool_height = pool_param['pool_height']
    pool_width  = pool_param['pool_width']
    stride      = pool_param['stride']

    H_prima = int(1 + (H - pool_height) / stride)
    W_prima = int(1 + (W - pool_width) / stride)

    dx = np.zeros_like(x)

    for n in range(N):
        for c in range(C):
            for h_prima in range(H_prima):
                for w_prima in range(W_prima):
                    # Defino los 4 puntos que determinan la ventana del filtro
                    h1 = h_prima * stride
                    h2 = h_prima * stride + pool_height
                    w1 = w_prima * stride
                    w2 = w_prima * stride + pool_width

                    # Le aplico la ventana a la entrada
                    window = x[n, c, h1:h2, w1:w2]
                    window2 = np.reshape(window, (pool_height*pool_width))

                    # Obtengo una ventana como la anterior pero con uno en la posición
                    # del mayor elemento y ceros en el resto, esta ventana la vamos
                    # a utilizar para calcular el gradiente según x
                    window3 = np.zeros_like(window2)
                    window3[np.argmax(window2)] = 1

                    # Como la función es un máx multiplicamos la matriz anterior por
                    # el gradiente que nos viene para calcular dx
                    dx[n,c,h1:h2,w1:w2] = np.reshape(window3,(pool_height,pool_width)) * dout[n,c,h_prima,w_prima]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    N, C, H, W = x.shape

    out, cache = None, None
    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization using the vanilla   #
    # version of batch normalization defined above. Your implementation should#
    # be very short; ours is less than five lines.                            #
    ###########################################################################
    x_reshaped = x.swapaxes(0,1).reshape(C,N*H*W).swapaxes(0,1)
    out, cache = batchnorm_forward(x_reshaped, gamma, beta, bn_param)
    out        = out.swapaxes(0,1).reshape(C,N,H,W).swapaxes(0,1)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    N, C, H, W = dout.shape

    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization using the vanilla   #
    # version of batch normalization defined above. Your implementation should#
    # be very short; ours is less than five lines.                            #
    ###########################################################################
    dout_reshaped     = dout.swapaxes(0,1).reshape(C,N*H*W).swapaxes(0,1)
    dx, dgamma, dbeta = batchnorm_backward( dout_reshaped, cache )
    dx                = dx.swapaxes(0,1).reshape(C,N,H,W).swapaxes(0,1)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx
