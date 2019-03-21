# coding=utf-8
import os
import logging
import time
from retry import retry
from enum import Enum
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale_cli.openscale.openscale import OpenScale

logger = logging.getLogger(__name__)
parent_dir = os.path.dirname(__file__)

class OpenScaleReset(OpenScale):

    def __init__(self, args, credentials, database_credentials):
        super().__init__(args, credentials, database_credentials)

    def reset(self, reset_type):
        if reset_type is ResetType.METRICS:
            self.reset_metrics()
        elif reset_type is ResetType.MONITORS:
            self.reset_metrics()
            self.reset_monitors()
        # "factory reset" the system
        elif reset_type is ResetType.DATAMART:
            self.delete_datamart()
            self.clean_database()

    @retry(tries=5, delay=4, backoff=2)
    def reset_metrics(self):
        '''
        Clean up the payload logging table, monitoring history tables etc, so that it restores the system
        to a fresh state with datamart configured, model deployments added, all monitors configured,
        but no actual metrics in the system yet. The system is ready to go.
        '''
        logger.info('Deleting datamart metrics ...')
        if self._database is None:
            logger.info('No database specified OR metrics for {} internal database instance cannot be reset'.format(self._args.service_name))
        else:
            self._database.reset_metrics_tables(self._datamart_name)
            logger.info('Datamart metrics deleted successfully')

    @retry(tries=5, delay=4, backoff=2)
    def reset_monitors(self):
        '''
        Remove all configured monitors and corresponding metrics and history, but leave the actual model deployments
        (if any) in the datamart. User can proceed to configure the monitors via user interface, API, or fastpath.
        '''
        logger.info('Deleting datamart monitors ...')
        subscription_uids = self._client.data_mart.subscriptions.get_uids()
        for subscription_uid in subscription_uids:
            try:
                start = time.time()
                subscription = self._client.data_mart.subscriptions.get(subscription_uid)
                elapsed = time.time() - start
                logger.debug('TIMER: data_mart.subscriptions.get in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.explainability.disable()
                elapsed = time.time() - start
                logger.debug('TIMER: subscription.explainability.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.fairness_monitoring.disable()
                elapsed = time.time() - start
                logger.debug('TIMER: subscription.fairness_monitoring.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.performance_monitoring.disable()
                elapsed = time.time() - start
                logger.debug('TIMER: subscription.performance_monitoring.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.payload_logging.disable()
                elapsed = time.time() - start
                logger.debug('TIMER: subscription.payload_logging.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.quality_monitoring.disable()
                elapsed = time.time() - start
                logger.debug('TIMER: subscription.quality_monitoring.disable in {:.3f} seconds'.format(elapsed))
                logger.info('Datamart monitors deleted successfully')
            except Exception as e:
                logger.warning('Problem during monitor reset: {}'.format(str(e)))

        # finally, drop the monitor-related tables
        if self._database is None:
            logger.info('No database specified OR monitor-related tables for {} internal database instance cannot be reset'.format(self._args.service_name))
        else:
            self._database.drop_metrics_tables(self._datamart_name)

    @retry(tries=5, delay=4, backoff=2)
    def delete_datamart(self):
        logger.info('Deleting datamart (if already present) ...')
        try:
            start = time.time()
            self._client.data_mart.delete()
            elapsed = time.time() - start
            logger.debug('TIMER: data_mart.delete in {:.3f} seconds'.format(elapsed))
            logger.info('Datamart deleted successfully')
        except Exception as e:
            ignore_exceptions = ['AIQCS0005W', 'AIQC50005W', 'AISCS0005W'] # datamart does not exist, so cannot delete
            if any(word in str(e) for word in ignore_exceptions):
                logger.debug(e)
                logger.info('Datamart not present')
            else:
                raise e

    @retry(tries=5, delay=4, backoff=2)
    def clean_database(self):
        logger.info('Cleaning database ...')
        if self._database is None:
            logger.info('No database specified OR table/schema for {} internal database instance cannot be removed'.format(self._args.service_name))
        else:
            self._database.drop_existing_schema(self._datamart_name, self._keep_schema)
            logger.info('Database cleaned successfully')
