from webgeodyn.models import Model
import numpy as np


def coeffilter(coeffilter_function):
    """ Decorator for filters only applied to the coefficients of spherical harmonics.

    The functions decorated by this decorator take coefs as the first parameter and return filtered coefs.
    """
    def applyfilter(model, *args, **kwargs):
        if "copy" in kwargs and kwargs["copy"]:
            returnedModel = model.copy()
        else:
            returnedModel = model

        if "measureName" not in kwargs or kwargs["measureName"] is None:
            # Filter is called on the whole model, applying the filter to all measures
            measurelist = model.measures.keys()
        elif type(kwargs["measureName"]) == list:
            measurelist = kwargs["measureName"]
        else:
            measurelist = [kwargs["measureName"],]

        if "copy" in kwargs:
            del kwargs["copy"]
        if "measureName" in kwargs:
            del kwargs["measureName"]

        for measureName in measurelist:
            if measureName not in model.measures:
                raise ValueError(measureName + " is not inside given model measures.")

            new_coefs = coeffilter_function(returnedModel.measures[measureName].data, *args, **kwargs)
            returnedModel.measures[measureName].setData(new_coefs)

        returnedModel.clearCache()
        return returnedModel
    return applyfilter


def coeffilter_norealisations(coeffilter_function):
    """ Decorator for coeffilters that do not handle realisations.

        The functions decorated by this decorator take coefs as the first parameter and return filtered coefs.
    """
    def applyfilter(model, *args, **kwargs):
        if "copy" in kwargs and kwargs["copy"]:
            returnedModel = model.copy()
        else:
            returnedModel = model

        if "measureName" not in kwargs or kwargs["measureName"] is None:
            # Filter is called on the whole model, applying the filter to all measures
            measurelist = model.measures.keys()
        elif type(kwargs["measureName"]) == list:
            measurelist = kwargs["measureName"]
        else:
            measurelist = [kwargs["measureName"],]

        if "copy" in kwargs:
            del kwargs["copy"]
        if "measureName" in kwargs:
            del kwargs["measureName"]

        for measureName in measurelist:
            if measureName not in model.measures:
                raise ValueError(measureName + " is not inside given model measures.")

            if returnedModel.measures[measureName].has_realisations:
                new_coefs = None
                nreal = returnedModel.measures[measureName].data.shape[2]
                for ireal in range(nreal):
                    new_realisation = coeffilter_function(returnedModel.measures[measureName].data[:,:,ireal],*args)
                    if new_coefs is None:
                        new_coefs = np.zeros((new_realisation.shape[0],new_realisation.shape[1],nreal))
                    new_coefs[:,:,ireal] = new_realisation
            else:
                new_coefs = coeffilter_function(returnedModel.measures[measureName].data,*args, **kwargs)
            returnedModel.measures[measureName].setData(new_coefs)

        returnedModel.clearCache()
        return returnedModel
    return applyfilter


def measurefilter(measurefilter_function):
    """ Decorator for filters only applied to measures.

        The functions decorated by this decorator take measures as the first parameter and return the filtered measures.
    """
    def applyfilter(model, *args, **kwargs):
        if "copy" in kwargs and kwargs["copy"]:
            returnedModel = model.copy()
        else:
            returnedModel = model

        if "measureName" not in kwargs or kwargs["measureName"] is None:
            # Filter is called on the whole model, applying the filter to all measures
            measurelist = model.measures.keys()
        elif type(kwargs["measureName"]) == list:
            measurelist = kwargs["measureName"]
        else:
            measurelist = [kwargs["measureName"],]

        if "copy" in kwargs:
            del kwargs["copy"]
        if "measureName" in kwargs:
            del kwargs["measureName"]

        for measureName in measurelist:
            if measureName not in model.measures:
                raise ValueError(measureName + " is not inside given model measures.")

            new_measure = measurefilter_function(returnedModel.measures[measureName],*args, **kwargs)
            returnedModel.measures[measureName] = new_measure

        returnedModel.clearCache()
        return returnedModel
    return applyfilter


def modelfilter(modelfilter_function):
    """ Decorator for filters directly applied to the model.

        The functions decorated by this decorator take the model as first parameter and return the filtered model.
    """
    def applyfilter(model, *args, **kwargs):
        if "copy" in kwargs and kwargs["copy"]:
            returnedModel = model.copy()
        else:
            returnedModel = model

        if "copy" in kwargs:
            del kwargs["copy"]

        returnedModel = modelfilter_function(returnedModel, *args, **kwargs)

        returnedModel.clearCache()
        return returnedModel
    return applyfilter
