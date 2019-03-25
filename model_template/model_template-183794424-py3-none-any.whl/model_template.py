import logging.config
import logging

from abc import ABC, abstractmethod

logging.config.fileConfig('./model_template/logging.conf')
logger = logging.getLogger('template_logger')

class ModelTemplate(ABC):

    def __init__(self):
        self._model = self._load_model()

    @abstractmethod
    def _load_model(self):
        """
        Function that implements load model, is recommended load
        the model with training step off
        """
        pass

    @abstractmethod
    def _parse_data(self):
        """
        Treats the data to be inserted into the model
        """
        pass
 
    @abstractmethod
    def _model_output(self):
        """
        Return the output of model, if you are running a neural network
        return the values off the last layer, don't use binarizer or return
        the final classification in this function
        """
        pass

    @abstractmethod
    def _recover_label(self, model_output):
        """
        Recover the label
        """
        pass

    def predict(self, data):
        """
        Run the model and return the prediction
        """

        logger.info('Make prediction')

        logger.debug('Parsing data')
        data = self._parse_data(data)
        logger.debug('Data parsed')

        logger.debug('Getting output from model')
        output = self._model_output(data)
        logger.debug('Output taked successfully')

        logger.debug('Transforming output in label')
        prediction = self._recover_label(output)
        logger.debug('The result label is: [%s]' % prediction)

        logger.info('Finish prediction')

        return prediction
