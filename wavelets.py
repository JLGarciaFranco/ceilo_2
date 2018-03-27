"""
Wavelet Covariant Transform Algorithm
**************************************
.. toctree::
   :maxdepth: 2


Description
------------

This toolbox contains functions used in the retrieval of the mixed-layer height following a wavelet covariant transform algorithm, from
:cite:`brooks2003`. Roughly, this method compares the local match or similarity between the Haar wavelet function and the backscattering profile.
This could be interpreted as pattern search for a sudden jump. In fact, this same procedure is used to analyze electric signals and
find electric jumps.

The code is written to operate between functions that follow the recursive algorithm by :cite:Grabon2010.

* The four functions are.
    1. Main covariance transform. :meth:`wavelets.haarcovtransfm`.
    2. Find boundary-layer top. :meth:`wavelets.findtops`.
    3. Haar function. :meth:`wavelets.haarval`.
    4. Iterative inner-function :meth:`wavelets.firstmlh`.

"""
##########  Wavelet toolbox ############################
### Following Brooks (2003) and Grabon (2010) ###########
### by Jorge L. Garcia Franco on May-Aug 2016 ###########
### contact: jgcaspark@ciencias.unam.mx or hotmail.com ##
#########################################################
# Import numpy for math processing
import numpy as np
def haarcovtransfm(allprf,z1,i,a,f,t,tope,botom):
	r""" This function does something

   :param allprf: backscattering matrix, numpy array nxm dims
   :param z1: height vector, typically np.array ranging from 100 to 5000 m.
   :param i: index for current time value. (integer)
   :param a: Dilation type, string for either (Automated or Standard) see below for further explanation.
   :param f: Initial resolution between steps, integer.
   :param tope: Maximum height where mixed-layer or boundary layer can be obtained (float).
   :param botom: Minimum height [m] where mixed layer or BL can be obtained, float.
   :rtype: float: Residual Layer Height

   Formula adopted from :cite:`brooks2003`, Grabon2010]_.

   .. math:: W_f(a,b)=\frac{1}{a}\int_{z_0}^{z_{max}}B(z)H\bigg(\frac{(z-b)}{a}\bigg)).


   * :math:`W_f` Wavelet transform
   * :math:`a` Dilation value, in [m]
   * :math:`b` Wavelet translation, in [m]
   * :math:`z_0` Minimum integration level [m]
   * :math:`z_{max}` Maximum integration level [m]
   * :math:`B(z)` Backscaterring matrix

        Returns MLH, BLmin, BLmax

	"""
	global fi
	global z
	global a0
	global iz
	global b
	global top
	top=tope
	fi=f
	iz=int(f/2.)
	z=z1
## Bottom is 80 m due to noise generated artifacts by surface, newmlh is initially this value to jumpstart.
## wf = wavelet transform coefficients array, initially  empty.
	bottom=botom
	b=range(bottom,top,fi)
#	print b
# Selecting current profile for current time.
	prf=allprf[:,i]
# a = Automated implies following recursive algorithm for finding transition zone by algorithm of Brooks.
	if a=='Auto':
		a=240
		a0=40
		detail=True
# if not Automated, Standard implies using standard dilation a = 60m (found by Grabon and useful for UNAM profiles.
	elif a=='Standard':
		a=60
		detail=False
# Call recursive function to find mlh (clearing out bottom values, i.e., no floor mlh value is permitted.
# Inspect firstmlh function below if needed.
	newmlh,wf=firstmlh(prf,a,bottom)
# If Automated, find top, bot and mlh using recursive algorithm.
	if detail:
		bot,newmlh,top=findtops(prf,wf,newmlh,a)
	else:
		bot=newmlh
		top=newmlh
### RETURN MLH ####
	return bot,newmlh,top


#######################################################################################################################
### haarval = function to compute wavelet coefficient Wf(a,b) for every a,b.
def haarval(prf,a,b0):
    r"""

    Obtain haar value, compute every Wf(a,b)

    **Parameters**

    **prf**: `np.nadarray`
        backscattering profile at time ti
    **a** : `float`
        Wavelet dilation.
    **b0** : `float`
        Translation point in z.

    :rtype: float: Wavelet transform coefficient at dilation a and translation b.


    **Haar Wavelet**

    .. math:: h\bigg(\frac{z-b}{a}\bigg) = \begin{cases}       + 1 & b-\frac{a}{2}\leq z\leq 0 \\         -1 & b \leq z \leq b+\frac{a}{2} \\         0 & otherwise                 \end{cases}


    See Also
    --------

    findtops, haarcovtransfm

    """
    global z
    # wnlen is the window size to compute the positive and negative pulse.
    wnlen=a/2.
    fun=0
    # Loop through z. Assigning weight according to Haar.
    for i,z0 in enumerate(z):
    	if z0 < b0-wnlen or z0 == b0:
    		continue
    	elif z0 > b0+wnlen:
    		break
    	elif z0 >= b0-wnlen and z0 < b0:
    		fun=fun+prf[i]
    	elif z0 > b0 and z0 <= b0+wnlen:
    		fun=fun-prf[i]

    return fun/float(a)

#######################################################################################################################
### Function findtops, finds recursively the top and bottom of the transition zone, and mlh by
### finding the suitable dilation.
def findtops(prf,wf,newmlh,a):
    r"""
    **Boundary Layer Height and Entrainment layer thickness.**


    Find boundary layer top and bottom, similar to :cite:`brooks2003,Grabon2010`.
    This method follows a recursive method of analizying different dilations and translations, as a wavelet transform does.
    In this sense, we vary both `a` and `b` discretly. First `a` ranges from 120 [m] and decreases with a step of 20 [m] until the lowest dilation of 20 [m].
    Similarly, b varies from the bottom value to the top value in increments of 10 [m].

    **Parameters**

    **prf**: `np.nadarray`
        backscattering profile at time ti
    **wf** : `np.array wf(a_0,b)`
        Wavelet covariant transform coefficients.
    **newmlh** : `float`
        New mixed-layer value

    :rtype: array of floats: Bottom of entrainment layer, mixed-layer height and top of entrainment layer


    **Haar Wavelet recursive algorithm**

    The height of the bottom of the entrainment layer `E_L`, and the height top of the entrainment layer `E_U`
     are given by:

    .. math:: E_L=\frac{2}{5}W_f(a_0,b)
    .. math:: E_U=\frac{3}{5}W_f(a_0,b)

    See Also
    --------

    findtops, haarcovtransfm

    """
    ### First round of coefficients to find top (c1) and bottom (c2) heights.
    c1=0.6
    c2=0.4
    global a0
    bt=b
    while a>a0:
    	maxi=np.max(wf)
    	imaxi=np.argmax(wf)
    	#Top index retrieval
    	topindex=0
    	wf6=wf[imaxi]
    	while wf6 > c1*maxi and imaxi+topindex != len(wf)-1:
    		wf6=wf[imaxi+topindex]
    		topindex+=1
    	#Bottom index retrieval
    	botindex=1
    	wf4=wf[imaxi-botindex]
    	while wf4 > c2*maxi and imaxi-botindex!=0:
    		botindex+=1
    		wf4=wf[imaxi-botindex]
    	a=a-20
    	if bt[imaxi+topindex-1]-bt[imaxi]<=a0 or bt[imaxi]-bt[imaxi-botindex]:
    		break
    	bt=bt[imaxi-botindex:imaxi+topindex]
    	c1=c1-0.02
    	c2=c2+0.02
    	wf=[]
    	### Find wavelet transform coefficients given current dilation.
    	for n,b0 in enumerate(bt):
    		covtransform=haarval(prf,a,b0)
    		wf.append(covtransform)
    return bt[imaxi-botindex],bt[imaxi],bt[imaxi+topindex-1]
####################################################################################
### firstmlh: function to obtain first approximation to mlh given the first dilation observed.
### It is written to avoid ceiling or floor mlh values being floor = 200 and top =3000.
def firstmlh(prf,a,bottom):
    r""" **First mixed-layer height value**

    Retrieve first mixed layer-height value for initial dilation `a`..

    **Parameters**

    **prf**: `np.nadarray`
        backscattering profile at time ti
    **a** : `np.array wf(a_0,b)`
        Wavelet covariant transform coefficients.
    **bottom** : `float`
        Lowest allowed value for mixed layer height retrieval.

    :rtype: float: First mixed layer height value

    The mixed-layer height under \ref{brooks2003,Grabon2010} is given by the maximum of the wavelet covariance transfrom
    for a dilation `a` in a translation `b`, i.e.:

    .. math:: MLH=max(W_f(a,b))

    This script provides the first or only estimate of the MLH depending on how the script is run. If the recursive method is used then this
    MLH will change as the dilation changes, however, if the recursive method is not used then this MLH is exactly the maximum of
    `W_f(120,b)` where `a=120` is recommended by \ref{brooks2003} as the initial or only dilation value.

    See Also

    findtops, haarcovtransfm, haarval

    """
    index=0
    newmlh=bottom
    global b
    global top
    top=top-50
    #Loop until newmlh is not current bottomo or top
    while newmlh<=bottom+50 or newmlh >= top-50:
    	wf=[]
    	if newmlh>=top-50:
    		top=top-20
    	elif newmlh<=bottom+50:
    		bottom=bottom+20
    	index+=1
    	b=range(bottom,top,fi)
    	for n,b0 in enumerate(b):
    		covtransform=haarval(prf,a,b0)
    		wf.append(covtransform)
    	wf=np.asarray(wf)
    	try:
    		newmlh=b[np.argmax(wf)]
    	except:
    		break
    #		print newmlh
    #print bottom,top,newmlh
    return newmlh,wf
