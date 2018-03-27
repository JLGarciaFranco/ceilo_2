# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 12:13:43 2013

@author: wolf
"""
import numpy

def smooth(x,window_len=9,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """
    if type(x) == type([]):
        x = numpy.array(x)

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    # return the smoothed signal, chopping off the ends so that it has the previous size.
    return y[window_len-1:-window_len+1]

def adc_interp(signal, window='hanning', step_size=None):
    '''
        this function returns signal after trying to figure out the underlying
    analog signal that has been quantized (perhaps signifigantly) by an
    analog to digital converter.
        in this algorithm, only 'ambiguous' data are included in the convolution, 
    or considered in the interpolation.  To be considered ambiguous, 
    data points must be within +/- 1 quantized step_size of the actual 
    signal value.
    inputs:
        signal
        window_len=9   : the size of the window over which to average
                            "ambiguous" data.
    returns:
        interpolated_signal
    '''
    if step_size is None:
        # figure out the quantization step size.
        s = list(set(signal))
        s.sort()
        diffs = numpy.diff(s)
        step_size = numpy.median(diffs)
    
    window_lens = [129,17,11,9,5]
    step_sizes  = numpy.array([1.1, 1.4, 3.0, 6.5, 6.5])*step_size
    for window_len, step_size in zip(window_lens, step_sizes):
        print window_len,step_size
        # create a simple smooth normalized window to do weighted averages
        win = numpy.zeros(2*window_len, numpy.float64)
        win[window_len] = 1.0
        win = smooth(win, window_len=window_len, window=window)
        isig = []
        # how many points to go forward and backward
        fore = window_len/2
        aft  = window_len - fore 
        for i in xrange(len(signal)):
            ambiguous_data_pts = []
            awin = []
            for j in xrange(max(0,i-aft),min(len(signal),i+fore)):
                dj = j-i
                dwin = dj+window_len
                if abs(signal[j] - signal[i]) <= step_size*1.1:
                    ambiguous_data_pts.append(signal[j]*win[dwin])
                    awin.append(win[dwin])
            isig.append(numpy.sum(ambiguous_data_pts/numpy.sum(awin)))
        signal = numpy.array(isig)
    return numpy.array(isig)
    
    
    


