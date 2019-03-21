from __future__ import print_function
# 2017-05-05 Edward Ando and Emmanuel Roubin
import numpy
import scipy.ndimage

numpy.set_printoptions(precision=3, suppress=True)

# Point at which to consider no rotation
rotationAngleDegThreshold = 0.0001

###########################################################
# From components (translation, rotation, zoom, shear) compute F
###########################################################


def computeTransformationOperator(transformation, Fcentre=[0.0, 0.0, 0.0], Fpoint=[0.0, 0.0, 0.0]):
    """
    Builds "F", a 4x4 linear transformation operator from a dictionary of transformation parameters (translation, rotation, zoom, shear).
    F can be used to deform coordinates as follows:
    $$ F.x = x'$$

    Parameters
    ----------
        transformation : dictionary of 3x1 arrays
            Input to computeTransformationOperator is a "transformation" dictionary where all items are optional.

            Keys
                t = translation (z,y,x). Note: ( 0, 0, 0 ) does nothing
                r = rotation in "rotation vector" format. Note: ( 0, 0, 0 ) does nothing
                z = zoom. Note: ( 1, 1, 1 ) does nothing
                s = "shear". Note: ( 0, 0,0 ) does nothing

        Fcentre : 3x1 array, optional
            Point where F is centered (centre of rotation)

        Fpoint : 3x1 array, optional
           Point where F is going to be applied

    Returns
    -------
        F : 4x4 array of floats
            F, transformation operator

    Note
    ----
        Useful reference: Chapter 2 -- Rigid Body Registration -- John Ashburner & Karl J. Friston, although we use a symmetric shear
    """
    F = numpy.eye(4, dtype='<f4')

    # Translation:
    if 't' in transformation:
        tmp = numpy.eye(4, dtype='<f4')
        tmp[0:3, 3] = transformation['t']
        F = numpy.dot(F, tmp)

    # Rotation
    if 'r' in transformation:
        # https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula
        # its length is the rotation angle
        rotationAngleDeg = numpy.linalg.norm(transformation['r'])

        if rotationAngleDeg > rotationAngleDegThreshold:
            # its direction is the rotation axis.
            rotationAxis = transformation['r'] / rotationAngleDeg

            # positive angle is clockwise
            K = numpy.array([[0,       -rotationAxis[2],  rotationAxis[1]],
                             [rotationAxis[2],        0,         -rotationAxis[0]],
                             [-rotationAxis[1],  rotationAxis[0],          0]])

            # Note the numpy.dot is very important.
            R = numpy.eye(3) + (numpy.sin(numpy.deg2rad(rotationAngleDeg)) * K) + \
                ((1.0 - numpy.cos(numpy.deg2rad(rotationAngleDeg))) * numpy.dot(K, K))

            tmp = numpy.eye(4, dtype='<f4')
            tmp[0:3, 0:3] = R

            F = numpy.dot(F, tmp)

    # Zoom + Shear
    if 'z' in transformation or 's' in transformation:
        tmp = numpy.eye(4, dtype='<f4')

        if 'z' in transformation:
            # Zoom components
            tmp[0, 0] = 1.0/transformation['z'][0]
            tmp[1, 1] = 1.0/transformation['z'][1]
            tmp[2, 2] = 1.0/transformation['z'][2]

        if 's' in transformation:
            # Shear components
            tmp[0, 1] = transformation['s'][0]
            tmp[0, 2] = transformation['s'][1]
            tmp[1, 2] = transformation['s'][2]
            # Shear components
            tmp[1, 0] = transformation['s'][0]
            tmp[2, 0] = transformation['s'][1]
            tmp[2, 1] = transformation['s'][2]
        F = numpy.dot(F, tmp)

    # Apply F to the Fpoint of the "image" and add this translation to F
    # F[0:3,3] += Fpoint - numpy.dot( F[0:3,0:3], Fpoint )

    # compute distance between point to apply F and the point where F is centered (centre of rotation)
    dist = numpy.array(Fpoint) - numpy.array(Fcentre)

    # apply F to the given point and calculate its displacement
    F[0:3, 3] -= dist - numpy.dot(F[0:3, 0:3], dist)

    # check that determinant of F is sound
    if numpy.linalg.det(F) < 0.00001:
        print("computeTransformationOperator(): Determinant of F is very small, this is probably bad, transforming volume into a point.")

    return F


###########################################################
# Polar Decomposition of a given F into human readable components
###########################################################
def FtoTransformation(F, Fcentre=[0.0, 0.0, 0.0], Fpoint=[0.0, 0.0, 0.0]):
    """
        Get components out of a linear transformation operator "F"

        Parameters
        ----------
        F : 4x4 array
            The linear transformation operator "F"

        Fcentre : 3x1 array, optional
            Point where F was calculated

        Fpoint : 3x1 array, optional
           Point where F is going to be applied

        Returns
        -------
        transformation : dictionary of arrays

                - t = 3x1 array. Translation vector (z,y,x)
                - r = 3x1 array. Rotation in "rotation vector" format
                - U = 3x3 array. Right stretch tensor
                - G = 3x3 array. Eigen vectors * eigenvalues of strains, from which principal directions of strain can be obtained

    """
    # Check for singular F if yes quit
    try:
        numpy.linalg.inv(F)
    except numpy.linalg.linalg.LinAlgError:
        transformation = {'t': [numpy.nan]*3,
                          'r': [numpy.nan]*3,
                          'U': numpy.nan,
                          'G': numpy.nan
                          }
        return transformation

    # Check for NaNs if any quit
    if numpy.isnan(F).sum() > 0:
        transformation = {'t': [numpy.nan]*3,
                          'r': [numpy.nan]*3,
                          'U': numpy.nan,
                          'G': numpy.nan
                          }
        return transformation

    # Check for NaNs if any quit
    if numpy.isinf(F).sum() > 0:
        transformation = {'t': [numpy.nan]*3,
                          'r': [numpy.nan]*3,
                          'U': numpy.nan,
                          'G': numpy.nan
                          }
        return transformation

    ###########################################################
    # The little 3x3 transformation matrix
    ###########################################################
    littleF = F[0:3, 0:3].copy()
    # print(numpy.linalg.det(littleF))
    # print(numpy.linalg.inv(littleF))

    ###########################################################
    # Calculate transformation by undoing F on the Fpoint
    ###########################################################
    tra = F[0:3, 3].copy()
    # tra -= Fpoint - numpy.dot( littleF, Fpoint )

    # compute distance between given point and the point where F was calculated
    dist = numpy.array(Fpoint) - numpy.array(Fcentre)

    # apply F to the given point and calculate its displacement
    tra -= dist - numpy.dot(F[0:3, 0:3], dist)

    ###########################################################
    # Polar decomposition of little 3x3 transformation matrix F[0:3, 0:3] = RU
    # U is the right stretch tensor
    # R is the rotation tensor
    ###########################################################
    
    # Compute the Right Cauchy tensor
    C = numpy.dot(littleF.T, littleF)
    
    # Solve eigen problem
    CeigVal, CeigVec = numpy.linalg.eig(C)

    # 2018-06-29 OS & ER check for negative eigenvalues
    # test "really" negative eigenvalues
    if CeigVal.any()/CeigVal.mean() < -1:
        print("transformationOperator.FtoTransformation(): negative eigen value in transpose(F).F which is really wrong. Exiting")
        print("Eigenvalues are: {}".format(CeigenVal))
        exit()
    # for negative eigen values but close to 0 we set it to 0
    CeigVal[CeigVal < 0] = 0

    # Diagonalise C --> which is U**2
    diagUsqr = numpy.array([[CeigVal[0], 0, 0],
                            [0, CeigVal[1], 0],
                            [0, 0, CeigVal[2]]])
    
    diagU = numpy.sqrt(diagUsqr)

    # 2018-02-16 check for both issues with negative (Udiag)**2 values and inverse errors
    try:
        U = numpy.dot(numpy.dot(CeigVec, diagU), CeigVec.T)
        R = numpy.dot(littleF, numpy.linalg.inv(U))
    except numpy.linalg.LinAlgError:
        #print("Error while inverting U in order to create the rotation matrix. Might come from singular little F.")
        #print("Little F =")
        #print(littleF)
        #print("returning null transformations.")
        transformation = {'t': [0, 0, 0],
                          'r': [0, 0, 0],
                          'U': numpy.eye(3),
                          'G': 3*[0, 0, 0]
                          }
        return transformation

    # print(CeigVal)
    # print(diagUsqr)
    # print(diagU)
    # print(U)
    # print(R)

    # normalisation of rotation matrix in order to respect basic properties
    # otherwise it gives errors like trace(R) > 3
    # this issue might come from numerical noise.
    # ReigVal, ReigVec = numpy.linalg.eig(R)

    for i in range(3):
        R[i, :] /= scipy.linalg.norm(R[i, :])
    # print("traceR - sumEig = {}".format(R.trace() - ReigVal.sum()))
    # print("u.v = {}".format(numpy.dot(R[:, 0], R[:, 1])))
    # print("detR = {}".format(numpy.linalg.det(R)))

    # Calculate rotation angle
    # Detect an identity -- zero rotation
    # if numpy.allclose(R, numpy.eye(3),  atol=1e-03):
    #     rotationAngleRad = 0.0
    #     rotationAngleDeg = 0.0

    # Detect trace(R) > 3 (should not append but appends)
    arccosArg = 0.5 * (R.trace() - 1.0)
    if arccosArg > 1.0:
        rotationAngleRad = 0.0
    else:
        # https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Rotation_matrix_.E2.86.94_Euler_axis.2Fangle
        rotationAngleRad = numpy.arccos(arccosArg)
    rotationAngleDeg = numpy.rad2deg(float(rotationAngleRad))

    # print("R")
    # print(R)
    # print("trace R = {}".format(R.trace()))
    # print("arccosArg = {}".format(arccosArg))
    # print("rotationAngleRad = {}".format(rotationAngleRad))
    # print("rotationAngleDeg = {}".format(rotationAngleDeg))

    if rotationAngleDeg > rotationAngleDegThreshold:
        rotationAxis = numpy.array([R[2, 1] - R[1, 2],
                                    R[0, 2] - R[2, 0],
                                    R[1, 0] - R[0, 1]])
        rotationAxis /= 2.0 * numpy.sin(rotationAngleRad)
        rot = rotationAngleDeg * rotationAxis
    else:
        rot = [0.0, 0.0, 0.0]
    ###########################################################

    # print "R is \n", R, "\n"
    # print "|R| is ", numpy.linalg.norm(R), "\n"
    # print "det(R) is ", numpy.linalg.det(R), "\n"
    # print "R.T - R-1 is \n", R.T - numpy.linalg.inv( R ), "\n\n"

    # print "U is \n", U, "\n"
    # print "U-1 is \n", numpy.linalg.inv( U ), "\n\n"

    # Also output eigenvectors * their eigenvalues as output:
    G = []

    for eigenvalue, eigenvector in zip(CeigVal, CeigVec):
        G.append(numpy.multiply(eigenvalue, eigenvector))

    transformation = {'t': [t for t in tra],
                      'r': [r for r in rot],
                      'U': U,
                      'G': G
                      }

    return transformation


###########################################################
# Taken an F and apply it (C++) to an image
###########################################################
def applyTransformationOperator(im, F=None, Fpoint=None, interpolationOrder=1):
    """
        Deform a 3D image using a transformation operator "F", applied using spam's C++ interpolator.

        Parameters
        ----------
        im : 3D number array
            3D number array of grey levels to be deformed

        F : 4x4 array, optional
            "F" linear transformation operator.
            Highly recommended additional argument (why are you calling this function otherwise?)

        Fpoint : 3x1 array of floats, optional
            Centre of application of F.
            Default = (numpy.array(im1.shape)-1)/2.0
            i.e., the centre of the image

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 1

        Returns
        -------
        imDef : 3D array
            Deformed greyscales by F
    """
    # import sys
    # import os
    from . import DICToolkit

    # Sort out F and calculate inverse
    if F is None:
        Finv = numpy.eye(4, dtype='<f4')
    else:
        try:
            Finv = numpy.linalg.inv(F).astype('<f4')
        except numpy.linalg.linalg.LinAlgError:
            # print( "\tapplyTransformationOperator(): Can't inverse F, setting it to identity matrix. F is:\n{}".format( F ) )
            Finv = numpy.eye(4, dtype='<f4')

    if Fpoint is None:
        Fpoint = (numpy.array(im.shape)-1)/2.0

    imDef = numpy.zeros_like(im, dtype='<f4')

    if interpolationOrder > 1:
        print("DIC.transformationOperator.applyTransformationOperator(): interpolation Order > 1 not implemented")
        return

    im = im.astype('<f4')
    Fpoint = numpy.array(Fpoint).astype('<f4')

    # We need to inverse F for question of direction
    DICToolkit.applyTransformationOperatorC(im, imDef, Finv, Fpoint, int(interpolationOrder))

    return imDef


###########################################################
# Taken an F and apply it (slowly) to an image
###########################################################
def applyTransformationOperatorPython(im, F=None, Fpoint=None, interpolationOrder=3):
    """
        Deform a 3D image using a transformation operator "F", applied using scipy.ndimage.map_coordinates

        Parameters
        ----------
        im : 3D number array
            3D number array of grey levels to be deformed

        F : 4x4 array, optional
            "F" linear transformation operator.
            Highly recommended additional argument (why are you calling this function otherwise?)

        Fpoint : 3x1 array of floats, optional
            Centre of application of F.
            Default = (numpy.array(im1.shape)-1)/2.0
            i.e., the centre of the image

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 3

        Returns
        -------
        imSub : 3D array
            Deformed greyscales by F
    """

    if F is None:
        Finv = numpy.eye(4, dtype='<f4')
    else:
        try:
            Finv = numpy.linalg.inv(F).astype('<f4')
        except numpy.linalg.linalg.LinAlgError:
            # print( "\tapplyTransformationOperatorPython(): Can't inverse F, setting it to identity matrix. F is:\n{}".format( F ) )
            Finv = numpy.eye(4)

    if Fpoint is None:
        Fpoint = (numpy.array(im.shape)-1)/2.0

    imDef = numpy.zeros_like(im, dtype='<f4')

    coordinatesInitial = numpy.ones((4, im.shape[0] * im.shape[1] * im.shape[2]), dtype='<f4')

    coordinates_mgrid = numpy.mgrid[0:im.shape[0],
                                    0:im.shape[1],
                                    0:im.shape[2]]

    # Copy into coordinatesInitial
    coordinatesInitial[0, :] = coordinates_mgrid[0].ravel() - Fpoint[0]
    coordinatesInitial[1, :] = coordinates_mgrid[1].ravel() - Fpoint[1]
    coordinatesInitial[2, :] = coordinates_mgrid[2].ravel() - Fpoint[2]

    # Apply F to coordinates
    coordinatesDef = numpy.dot(Finv, coordinatesInitial)

    coordinatesDef[0, :] += Fpoint[0]
    coordinatesDef[1, :] += Fpoint[1]
    coordinatesDef[2, :] += Fpoint[2]

    imDef += scipy.ndimage.map_coordinates(im,
                                           coordinatesDef[0:3],
                                           order=interpolationOrder).reshape(imDef.shape).astype('<f4')
    return imDef

###############################################################
# Taken a field of F and apply it (quite slowly) to an image
###############################################################


def applyTransformationOperatorField(im, fieldName=None, fieldCoords=None, fieldValues=None, fieldBinRatio=1.0, neighbours=8, interpolationOrder=3, verbose=False):
    """
        Deform a 3D image using a field of transformation operators "F" coming from a regularGrid,
        applied using scipy.ndimage.map_coordinates.

        Parameters
        ----------
        im : 3D array
            3D array of grey levels to be deformed

        fieldName : string, optional
            Name of the file containing the transformation operators field

        fieldCoords: 2D array, optional
            nx3 array of n points coordinates (ZYX)
            centre where each transformation operator "F" has been calculated

        fieldValues: 3D array, optional
            nx4x4 array of n points transformation operators

        fieldBinRatio : int, optional
            If the input field refers to a binned version of the image
            `e.g.`, if ``fieldBinRatio = 2`` the ``fieldName`` values have been calculated
            for an image half the size of the input image ``im``
            Default = 1

        neighbours : int, optional
            Neighbours for field interpolation
            If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance.
            Default = 8

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 1

        Returns
        -------
        imDef : 3D array
            deformed greylevels by a field of transformation operators "F"
    """

    # Create the grid of the input image
    imSize = im.shape
    coordinates_mgrid = numpy.mgrid[0:imSize[0],
                                    0:imSize[1],
                                    0:imSize[2]]

    coordIn = numpy.ones((imSize[0] * imSize[1] * imSize[2], 4))

    coordIn[:, 0] = coordinates_mgrid[0].ravel()
    coordIn[:, 1] = coordinates_mgrid[1].ravel()
    coordIn[:, 2] = coordinates_mgrid[2].ravel()

    numberofPoints = imSize[0] * imSize[1] * imSize[2]

    # Copy initial coordinates to the deformed coordinates
    coordDef = coordIn.copy()

    # Read input Ffield, usually the result of a regularGrid correlation
    if fieldName:
        import spam.helpers.tsvio
        FfromFile = spam.helpers.tsvio.readTSV(fieldName, fieldBinRatio=fieldBinRatio)
        fieldCoords = FfromFile["fieldCoords"]
        fieldValues = FfromFile["Ffield"]
    else:
        fieldCoords = fieldCoords
        fieldValues = fieldValues

    # Create the k-d tree of the coordinates of the input F field
    from scipy.spatial import KDTree
    tree = KDTree(fieldCoords)

    # Loop over each point of the grid of the input image
    for point in range(coordIn.shape[0]):
        if verbose:
            print("\rWorking on point {} {}%".format(point, (point/float(numberofPoints))*100), end='')

        # Calculate the distance of the current point to the points of the input F field
        distance, indices = tree.query(coordIn[point][0:3], k=neighbours)

        # Check if we've hit the same point
        if numpy.any(distance == 0):

            # Deform the coordinates of the current point
            # by subtracting the translation part of the transformation operator F
            coordDef[point][:3] -= fieldValues[indices][numpy.where(distance == 0)][0][0:3, -1].copy()

        # Check if we have asked only for the closest neighbour
        elif neighbours == 1:

            # Deform the coordinates of the current point
            # by subtracting the translation part of the transformation operator F
            # applied on the current point
            coordDef[point][:3] -= FtoTransformation(fieldValues[indices].copy(),
                                                     Fcentre=fieldCoords[indices],
                                                     Fpoint=coordIn[point][:3])["t"]

        # Consider the k closest neighbours
        else:
            # Compute the `Inverse Distance Weighting` since the closest points should have the major influence
            weightSumInv = sum(1/distance)

            # Loop over each neighbour
            for neighbour in range(neighbours):
                # Calculate its weight
                weightInv = (1/distance[neighbour])/float(weightSumInv)

            # Deform the coordinates of the current point
            # by subtracting the translation part of the transformation operator F
            # applied on the current point
            # multiplied by the weight of each neighbour
                coordDef[point][:3] -= numpy.dot(FtoTransformation(fieldValues[indices][neighbour].copy(),
                                                                   Fcentre=fieldCoords[indices][neighbour],
                                                                   Fpoint=coordIn[point][:3])["t"],
                                                 weightInv)

    # Deform the image
    imDef = numpy.zeros_like(im)

    imDef += scipy.ndimage.map_coordinates(im,
                                           coordDef[:, 0:3].T,
                                           mode="constant",
                                           order=interpolationOrder).reshape(imDef.shape).astype('<f4')

    return imDef


def correctFfield(fileName=None,
                  fieldCoords=None, fieldValues=None, fieldRS=None, fieldDF=None, fieldPSCC=None, fieldIT=None,
                  fieldBinRatio=1.0,
                  ignoreBadPoints=False, ignoreBackGround=False,
                  correctBadPoints=False,
                  deltaFnormMin=0.001, pixelSearchCCmin=0.98,
                  neighbours=12,
                  filterPoints=False, filterPointsRadius=3,
                  verbose=False,
                  saveFile=False, saveFileName=None):
    """
    This function corrects a field of transformation operators **F** calculated at a number of points.
    This is typically the output of the DICdiscrete and DICregularGrid clients.
    The correction is done based on the `SubPixelReturnStatus` and `SubPixelDeltaFnorm` of the correlated points.
    It takes as an input either a tsv file containing the result of the correlation or
    6 separate arrays:

      1 the coordinates of the points

      2 the Ffield

      3 the `SubPixelReturnStatus` 

      4 the `SubPixelDeltaFnorm` 

      5 the `PSCC` 

      6 the `SubPixelIterations` 


    Parameters
    ----------
        fileName : string, optional
            name of the file

        fieldCoords : 2D array, optional
            nx3 array of n points coordinates (ZYX)
            centre where each transformation operator **F** has been calculated

        fieldValues : 3D array, optional
            nx4x4 array of n points transformation operators

        fieldRS : 1D array, optional
            nx1 array of n points `SubPixelReturnStatus` from the correlation

        fieldDf : 1D array, optional
            nx1 array of n points `SubPixelDeltaFnorm` from the correlation

        fieldIT : 1D array, optional
            nx1 array of n points `SubPixelIterations` from the correlation

        fieldPSCC : 1D array, optional
            nx1 array of n points `PixelSearchCorrelationCoefficient` from the correlation

        fieldBinRatio : int, optional
            if the input field is referred to a binned version of the image
            *e.g.*, if `fieldBinRatio = 2` the fileName values have been calculated for an image half the size of what the returned Ffield is referring to.
            Default = 1.0

        ignoreBadPoints : bool, optional
            if True it will replace the **F** matrices of the badly correlated points with nans.
            Bad points are set according to `SubPixelReturnStatus` and `SubPixelDeltaFnorm` or `PSCC` of the correlation.
            Default = False

         ignoreBackGround : bool, optional
            if True it will replace the **F** matrices of the back ground points with nans.
            Back ground points are set according to `SubPixelReturnStatus` (<-4) of the correlation.
            Default = False

        correctBadPoints : bool, optional
            if True it will replace the **F** matrices of the badly correlated points with the weighted function of the k nearest good points.
            Bad points are set according to `SubPixelReturnStatus` and `SubPixelDeltaFnorm` or `PSCC` of the correlation
            The number of the nearest good neighbours can be defined (see `neighbours` below).
            Default = False

        deltaFnormMin: float, optional
            minimum value of subpixel change in F to consider a point with `SubPixelReturnStatus` = 1 as good or bad.
            Default = 0.001

        picelSearchCCmin: float, optional
            minimum value of pixel search correlation coefficient to consider a point as good or bad.
            Default = 0.98

        neighbours : int, optional
            if `correctBadPoints` is activated, it specifies the number of the nearest neighbours to consider.
            If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance.
            Default = 12

        filterPoints : bool, optional
            if True: a median filter will be applied on the **F** of each point.
            Default = False

        filterPointsRadius : int, optional
            Radius of median filter.
            Size of cubic structuring element is 2*filterPointsRadius+1.
            Default = 3

        verbose : bool, optional
            follow the progress of the function.
            Default = False

        saveFile : bool, optional
            save the corrected file into a tsv
            Default = False

        saveFileName : string, optional
            The file name for output.
            Default = 'spam'

    Returns
    -------
        Ffield : nx4x4 array
            n points transformation operators **F** after the correction

    """
    import os
    # read the input arguments
    if fileName:
        if not os.path.isfile(fileName):
            print("\n\ttransformationOperator.correctFfield():{} is not a file. Exiting.".format(fileName))
            return
        else:
            import spam.helpers.tsvio
            fi = spam.helpers.tsvio.readTSV(fileName, fieldBinRatio=fieldBinRatio, readDisplacements=True, readFs=False, readConvergence=True, readPixelSearchCC=True)
            Ffield = fi["Ffield"]
            fieldCoords = fi["fieldCoords"]
            fieldDims = fi["fieldDims"]
            RS = fi["SubPixReturnStat"]
            deltaFnorm = fi["SubPixDeltaFnorm"]
            iterations = fi["SubPixIterations"]
            PSCC = fi["PixelSearchCC"]
    elif fieldCoords is not None and fieldValues is not None and fieldRS is not None and fieldDF is not None and fieldPSCC is not None and fieldIT is not None:
        fieldCoords = fieldCoords
        fieldDims = numpy.array([len(numpy.unique(fieldCoords[:, 0])), len(numpy.unique(fieldCoords[:, 1])), len(numpy.unique(fieldCoords[:, 2]))])
        Ffield = fieldValues
        RS = fieldRS
        deltaFnorm = fieldDF
        PSCC = fieldPSCC
        iterations = fieldIT
    else:
        print("\ttransformationOperator.correctFfield(): Not enough arguments given. Exiting.")
        return

    # check if it is a subPixel field or a pixel search field
    if numpy.nansum(PSCC)>0 and iterations.sum()==0:
        pixelSearch = True
        subPixel = False
    else:
        pixelSearch = False
        subPixel = True

    # define good and bad correlation points according to `SubPixelReturnStatus` and `SubPixelDeltaFnorm` or `PSCC`conditions
    if ignoreBackGround is False:
        if subPixel:
            goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaFnorm <= deltaFnormMin)))
            badPoints = numpy.where(numpy.logical_or(RS <= 0, numpy.logical_and(RS == 1, deltaFnorm > deltaFnormMin)))
        if pixelSearch:
            goodPoints = numpy.where(PSCC >= pixelSearchCCmin)
            badPoints = numpy.where(PSCC < pixelSearchCCmin)
    else:
        if subPixel:
            goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaFnorm <= deltaFnormMin)))
            badPoints = numpy.where(numpy.logical_or(numpy.logical_and(RS <= 0, RS >= -4), numpy.logical_and(RS == 1, deltaFnorm > deltaFnormMin)))
            backGroundPoints = numpy.where(RS < -4)
        if pixelSearch:
            goodPoints = numpy.where(numpy.logical_and(RS >= -4, PSCC >= pixelSearchCCmin))
            badPoints = numpy.where(numpy.logical_and(RS >= -4, PSCC < pixelSearchCCmin))
        backGroundPoints = numpy.where(RS < -4)
        Ffield[backGroundPoints] = numpy.nan

    # if asked, ignore the bad correlation points by setting their F to identity matrix
    if ignoreBadPoints:
        Ffield[badPoints] = numpy.eye(4)*numpy.nan

    # if asked, replace the bad correlation points with the weighted influence of the k nearest good neighbours
    if correctBadPoints:
        # create the k-d tree of the coordinates of good points, we need this to search for the k nearest neighbours easily
        #   for details see: https://en.wikipedia.org/wiki/K-d_tree &
        #   https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.query.html

        from scipy.spatial import KDTree
        treeCoord = KDTree(fieldCoords[goodPoints])

        # extract the F matrices of the bad points
        fieldBad = numpy.zeros_like(Ffield[badPoints])
        fieldBad[:, -1, :] = numpy.array([0, 0, 0, 1])

        # check if we have asked only for the closest neighbour
        if neighbours == 1:

            # loop over each bad point
            for badPoint in range(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint+1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: the index of the nearest neighbour (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to the nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=neighbours)

                # replace bad point's F with the F of the nearest good point
                fieldBad[badPoint][:-1] = Ffield[goodPoints][ind][:-1].copy()

            # replace the corrected F field
            Ffield[badPoints] = fieldBad

        # if we have asked for more neighbours
        else:

            # loop over each bad point
            for badPoint in range(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint+1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: k nearest neighbours (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to each of the ith nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=neighbours)

                # compute the "Inverse Distance Weighting" since the nearest points should have the major influence
                weightSumInv = sum(1/distance)

                # loop over each good neighbour point:
                for neighbour in range(neighbours):
                    # calculate its weight
                    weightInv = (1/distance[neighbour])/float(weightSumInv)

                    # replace the F components of the bad point with the weighted F components of the ith nearest good neighbour
                    fieldBad[badPoint][:-1] += Ffield[goodPoints][ind[neighbour]][:-1]*weightInv

            # replace the corrected F field
            Ffield[badPoints] = fieldBad
        # overwrite RS to the corrected
        RS[badPoints] = 2

    # if asked, apply a median filter of a specific size in the F field
    if filterPoints:
        if verbose: print("\nFiltering...")
        import scipy.ndimage
        filterPointsRadius = int(filterPointsRadius)

        Ffield[:, 0, 0] = scipy.ndimage.generic_filter(Ffield[:, 0, 0].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, 0] = scipy.ndimage.generic_filter(Ffield[:, 1, 0].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, 0] = scipy.ndimage.generic_filter(Ffield[:, 2, 0].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        Ffield[:, 0, 1] = scipy.ndimage.generic_filter(Ffield[:, 0, 1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, 1] = scipy.ndimage.generic_filter(Ffield[:, 1, 1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, 1] = scipy.ndimage.generic_filter(Ffield[:, 2, 1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        Ffield[:, 0, 2] = scipy.ndimage.generic_filter(Ffield[:, 0, 2].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, 2] = scipy.ndimage.generic_filter(Ffield[:, 1, 2].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, 2] = scipy.ndimage.generic_filter(Ffield[:, 2, 2].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        Ffield[:, 0, -1] = scipy.ndimage.generic_filter(Ffield[:, 0, -1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, -1] = scipy.ndimage.generic_filter(Ffield[:, 1, -1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, -1] = scipy.ndimage.generic_filter(Ffield[:, 2, -1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        if ignoreBackGround:
            Ffield[backGroundPoints] = numpy.nan

    if saveFile:
        # if asked, write the corrected Ffield into a TSV
        if saveFileName:
            outDir = os.path.dirname(saveFileName)
            prefix = os.path.splitext(os.path.basename(saveFileName))[0]
        elif fileName:
            outDir = os.path.dirname(fileName)
            prefix = os.path.splitext(os.path.basename(fileName))[0]
        elif saveFileName is None and fileName is None:
            outDir = "."
            prefix = "spam"

        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tF11\tF12\tF13\tZdisp\tF21\tF22\tF23\tYdisp\tF31\tF32\tF33\tXdisp\tSubPixReturnStat\tSubPixDeltaFnorm\tSubPixIterations\tPSCC"
        outMatrix = numpy.array([numpy.array(range(Ffield.shape[0])),
                                 fieldCoords[:, 0], fieldCoords[:, 1], fieldCoords[:, 2],
                                 Ffield[:, 0, 0],    Ffield[:, 0, 1],    Ffield[:, 0, 2],    Ffield[:, 0, 3],
                                 Ffield[:, 1, 0],    Ffield[:, 1, 1],    Ffield[:, 1, 2],    Ffield[:, 1, 3],
                                 Ffield[:, 2, 0],    Ffield[:, 2, 1],    Ffield[:, 2, 2],    Ffield[:, 2, 3],
                                 RS, deltaFnorm, iterations, PSCC]).T

        if filterPoints:
            title = "{}/{}-corrected-N{}-filteredRad{}.tsv".format(outDir, prefix, neighbours, filterPointsRadius)
        else:
            title = "{}/{}-corrected-N{}.tsv".format(outDir, prefix, neighbours)
        numpy.savetxt(title,
                      outMatrix,
                      fmt='%.7f',
                      delimiter='\t',
                      newline='\n',
                      comments='',
                      header=TSVheader)

    return Ffield


def interpolateField(fieldCoords, fieldValues, interpCoords, fieldInterpBinRatio=1):
    """
    Interpolate a field of transformation operators (F).

    Parameters
    ----------
    fieldCoords : nPointsField x 3 array
        Z Y X coordinates of points where ``fieldValues`` are defined

    fieldValues : nPointsField x 4 x 4 array
        F defined at ``fieldCoords``

    interpCoords : nPointsInterpolate x 3
        Z Y X coordinates of points to interpolate F for

    fieldInterpBinRatio : int, optional
        If the ``fieldCoords`` and ``fieldValues`` matrices refer to a binned version of the new coordintes.
        `e.g.`, if ``fieldInterpBinRatio = 2`` then ``fieldCoords`` and ``fieldValues`` have been calculated on an
        image half the size of what ``interpCoords`` are referring to.

    Returns
    -------
    interpValues : nPointsInterpolate x 4 x 4 array of Fs
    """

    # This version of the function will use scipy.ndimage.interpolation.map_coordinates().
    # It takes in a field, which means that our fieldValues F field MUST be regularly spaced.
    # Furthermore it takes points at integer values (voxels), so we have to convert from
    # positions in the F field, and the "real" voxel coordinates.
    # e.g., Our first measurement point is 12,12,12 and the node spacing is 20 pixels.
    # map_coordinates will access this first F 12,12,12 at a position [0,0,0] in the matrix of F values in space
    # The next F 32,12,12 at a position [1,0,0]
    # Define the output array
    output = numpy.zeros((interpCoords.shape[0], 4, 4))

    # 1. calculate node spacing and position of first point
    # Measure node spacing in all three directions:
    zUnique = numpy.unique(fieldCoords[:, 0])
    yUnique = numpy.unique(fieldCoords[:, 1])
    xUnique = numpy.unique(fieldCoords[:, 2])

    zSpacing = zUnique[1] - zUnique[0]
    ySpacing = yUnique[1] - yUnique[0]
    xSpacing = xUnique[1] - xUnique[0]

    if zSpacing == ySpacing and zSpacing == xSpacing:
        nodeSpacing = zSpacing

        # TopPoint -- Ask ER -- Elizabeth Regina -- Honni soit qui mal y pense
        taupPoihunt = [zUnique[0], yUnique[0], xUnique[0]]
        # print "Top point:", taupPoihunt

        nNodes = [int(1 + (zUnique[-1]-zUnique[0]) / zSpacing),
                  int(1 + (yUnique[-1]-yUnique[0]) / ySpacing),
                  int(1 + (xUnique[-1]-xUnique[0]) / xSpacing)]
    else:
        print("Not all node spacings are the same, help! {} {} {} ".format(
            zSpacing, ySpacing, xSpacing))
        return "moinsUn"

    # 2. reshape fieldValues into an Z*Y*X*Fy*Fx array for map_coordinates
    fieldValues = fieldValues.reshape([nNodes[0], nNodes[1], nNodes[2], 4, 4])

    # 3. Convert interpCoords into positions in reshaped F array
    # If we have a non-zero bin, scale coordinates
    interpCoords /= fieldInterpBinRatio

    # Remove top corner coords...
    interpCoords -= taupPoihunt
    # And divide by node spacing, now coords are in 0->1 format
    interpCoords /= float(nodeSpacing)

    # 4. Call map_coordinates and return
    # Loop over each component of F, so they are not interpolated together.
    for Fy in range(4):
        for Fx in range(4):
            output[:, Fy, Fx] = scipy.ndimage.interpolation.map_coordinates(
                fieldValues[:, :, :, Fy, Fx], interpCoords.T, order=1)

    # 5. Scale transformation by binning value
    output[:, 0:3, 3] *= fieldInterpBinRatio
    return output

def mergeRegularGridAndDiscrete(
                fileNameRegularGrid=None,
                fileNameDiscrete=None,
                labelled=None,
                alwaysLabel=True,
                saveFileName=None):
    """
    This function merges displacement fields from the DICregularGrid script and 
    the DICdiscrete script.
    This can be useful where there are large flat zones in the image that cannot
    be correlated with small correlation windows, but can be identified and 
    tracked with a DICdiscrete computation.

    Parameters
    -----------
        fileNameRegularGrid : string
            File name of TSV from DICregularGrid client.
            Default = None

        fileNameDiscrete : string
            File name of TSV from DICdiscrete client
            Default = None

        labelled : 3D numpy array of ints
            Labelled volume used for discrete computation
            Default = None

        alwaysLabel : bool
            If regularGrid point falls inside the label, should we use the
            label displacement automatically?
            Otherwise if the reggularGrid point has converged should we use that?
            Default = True (always use Label displacement)

        saveFileName : string
            Output filename
            Default = None

    Returns
    --------
        Output matrix, with number of rows equal to DICregularGrid with columns:
            "NodeNumber", "Zpos", "Ypos", "Xpos", "Zdisp", "Ydisp", "Xdisp", "SubPixDeltaFnorm", "SubPixReturnStat", "SubPixIterations"
    """
    import spam.helpers

    regGrid  = spam.helpers.readTSV(fileNameRegularGrid)
    discrete = spam.helpers.readTSV(fileNameDiscrete)

    output = numpy.zeros([regGrid['fieldCoords'].shape[0], 10]) 
    for n, gridPoint in enumerate(regGrid['fieldCoords'].astype(int)): 
        label = labelled[gridPoint[0], gridPoint[1], gridPoint[2]] 
        # First column is point number
        output[n,0] = n 
        # Next three columns are the position of the regular grid point
        output[n,1:4] = gridPoint 
        # Is the point inside a discrete label?
        if label == 0 or ( not alwaysLabel and regGrid['SubPixReturnStat'][n] == 2):
            # If we're not in a label, copy the results from DICregularGrid
            output[n,4:7] = regGrid['Ffield'][n][0:3,-1] 
            output[n,7] = regGrid['SubPixDeltaFnorm'][n]
            output[n,8] = regGrid['SubPixReturnStat'][n]
            output[n,9] = regGrid['SubPixIterations'][n]
        else:
            output[n,4:7] = spam.DIC.FtoTransformation( discrete['Ffield'][label], Fcentre=discrete['fieldCoords'][label], Fpoint=gridPoint )['t'] 
            output[n,7] = discrete['SubPixDeltaFnorm'][label]
            output[n,8] = discrete['SubPixReturnStat'][label]
            output[n,9] = discrete['SubPixIterations'][label]

    #displacements = output[:,4:7].reshape([regGrid['fieldDims'][0],
                                           #regGrid['fieldDims'][1],
                                           #regGrid['fieldDims'][2],
                                           #3])

    #plt.imshow( displacements[:,24,:,0], vmin=0, vmax=3, cmap='plasma'); plt.show()

    if saveFileName is not None:
        numpy.savetxt( saveFileName,
                       output,
                       header="NodeNumber\tZpos\tYpos\tXpos\tZdisp\tYdisp\tXdisp\tSubPixDeltaFnorm\tSubPixReturnStat\tSubPixIterations",
                       delimiter="\t" )

    return output, regGrid['fieldDims']

def binning( im,
             binning,
             returnCropAndCentre=False ):
    """
    This function downscales images by averaging NxNxN voxels together in 3D and NxN pixels in 2D.
    This is useful for reducing data volumes, and denoising data (due to averaging procedure).

    Parameters
    ----------
        im : 2D/3D numpy array
            Input measurement field

        binning : int
            The number of pixels/voxels to average together

        returnCropAndCentre: bool (optional)
            Return the position of the centre of the binned image
            in the coordinates of the original image, and the crop
            Default = False

    Returns
    -------
        imBin : 2/3D numpy array
            `binning`-binned array

        (otherwise if returnCropAndCentre): list containing:
            imBin,
            topCrop, bottomCrop
            centre of imBin in im coordinates (useful for re-stitching)
    Notes
    -----
        Here we will only bin pixels/voxels if they is a sufficient number of
        neighbours to perform the binning. This means that the number of pixels that
        will be rejected is the dimensions of the image, modulo the binning amount. 

        The returned volume is computed with only fully binned voxels, meaning that some voxels on the edges
        may be excluded.
        This means that the output volume size is the input volume size / binning or less (in fact the crop
        in the input volume is the input volume size % binning
    """
    twoD = False
    import DICToolkit

    if im.dtype == 'f8': im = im.astype('<f4')

    binning = int(binning)
    #print("binning = ", binning)

    dimsOrig = numpy.array(im.shape)
    #print("dimsOrig = ", dimsOrig)

    # Note: // is a floor-divide
    imBin = numpy.zeros(dimsOrig//binning, dtype=im.dtype)
    #print("imBin.shape = ", imBin.shape)

    # Calculate number of pixels to throw away
    offset = dimsOrig % binning
    #print("offset = ", offset)

    # Take less off the top corner than the bottom corner
    topCrop = offset // 2
    #print("topCrop = ", topCrop)
    topCrop = topCrop.astype('<i2')

    if len(im.shape) == 2:
        # pad them
        im = im[numpy.newaxis, ...]
        imBin = imBin[numpy.newaxis, ...]
        topCrop = numpy.array([ 0, topCrop[0], topCrop[1] ]).astype('<i2')
        offset  = numpy.array([ 0, offset[0],  offset[1]  ]).astype('<i2')
        twoD = True

    # Call C++
    if im.dtype == 'f4':
        print("Float binning")
        DICToolkit.binningFloat(im, imBin, topCrop, binning)
    elif im.dtype == 'u2':
        print("Uint 2 binning")
        DICToolkit.binningUInt(im, imBin, topCrop, binning)
    elif im.dtype == 'u1':
        print("Char binning")
        DICToolkit.binningChar(im, imBin, topCrop, binning)

    if returnCropAndCentre:
        centreBinned = (numpy.array(imBin.shape)-1)/2.0
        relCentOrig = offset+binning*centreBinned
        return [imBin, [topCrop, offset-topCrop],  relCentOrig]
    else:
        return imBin

if __name__ == "__main__":
    import numpy

    data = numpy.loadtxt(
        "../../data/0.7_nTX_COx_02-01-02-03-04-05-01-02regularMeshDisp.tsv", delimiter="\t", skiprows=1)

    fieldCoords = data[:, 1:4]
    fieldKinema = data[:, 4:7]

    fieldValues = numpy.zeros((fieldCoords.shape[0], 4, 4))
    for i, row in enumerate(fieldKinema):
        fieldValues[i] = numpy.eye(4)
        fieldValues[i, 0:3, 3] = row

    interpCoords = fieldCoords
    print(interpCoords[1620])
    print(interpolateField(fieldCoords, fieldValues,
                           interpCoords, fieldInterpBinRatio=1)[1620])

    exit()

    import tifffile as tf
    # import matplotlib.pyplot as plt

    transformation = {'t': [0.0, 0.0, 0.0],
                      'r': [15.0, 0.0, 0.0],
                      'z': [1.0, 1.0, 1.0],
                      's': [0.0, 0.0, 0.0]}

    im = tf.imread('../../data/snow.tif').astype('<f4')

    imDef = numpy.zeros_like(im, dtype='<f4')

    imCentre = [im.shape[0]/2.0,
                im.shape[1]/2.0,
                im.shape[2]/2.0]

    F = computeTransformationOperator(transformation, imCentre)
    print("The following is the input transformation")
    print(transformation)

    for k in ["t", "r"]:
        print("{}\t".format(k),)
        for item in transformation[k]:
            # print "{:0.2f}\t".format(item),
            print("{}\t".format(item),)
        print()

    print("\n\nThe following is the input F")
    print(F)

    # applyTransformationOperatorPython( im, imDef, F, 3 )
    imDef = applyTransformationOperatorPython(im, F, interpolationOrder=1)

    print("\n\n")
    backCalculatedTransformation = FtoTransformation(F, imCentre)
    for k in ["t", "r", "U", "G"]:
        print("{}\t".format(k),)
        for item in backCalculatedTransformation[k]:
            # print "{:0.2f}\t".format(item),
            print("{}\t".format(item),)
        print()

    # print backCalculatedTransformation

    tf.imsave("../../data/snow-def.tif", imDef)

    # import sys, os
    # sys.path.append(os.path.join(os.path.dirname(__file__), "applyTransformationOperatorC"))
    # import applyTransformationOperatorC

    # print applyTransformationOperatorC.applyTransformationOperator( im, imDef, numpy.zeros((4,4,4), dtype='<f4'), 4 )
    # applyTransformationOperatorC.applyTransformationOperator( im, imDef, F )

    # #plt.imshow( imDef.reshape( im.shape ) )
    # plt.show()
