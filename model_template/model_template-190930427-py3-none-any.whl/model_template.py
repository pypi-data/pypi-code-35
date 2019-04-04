import logging
# import logging.config
# import pkg_resources

from abc import ABC, abstractmethod

# logging.config.fileConfig(logger_path)
# logger = logging.getLogger('template_logger')

logger = logging.getLogger()


class ModelTemplate(ABC):

    def __init__(self):
        self._model = self.load_model()

    @abstractmethod
    def load_model(self):
        """
        Function that implements load model, is recommended load
        the model with training step off
        """
        pass

    @abstractmethod
    def parse_data(self):
        """
        Treats the data to be inserted into the model
        """
        pass

    @abstractmethod
    def model_output(self):
        """
        Return the output of model, if you are running a neural network
        return the values off the last layer, don't use binarizer or return
        the final classification in this function
        """
        pass

    @abstractmethod
    def recover_label(self, model_output):
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
        data = self.parse_data(data)
        logger.debug('Data parsed')

        logger.debug('Getting output from model')
        output = self.model_output(data)
        logger.debug('Output taked successfully')

        logger.debug('Transforming output in label')
        prediction = self.recover_label(output)
        logger.debug('The result label is: [%s]' % prediction)

        logger.info('Finish prediction')

        return prediction
