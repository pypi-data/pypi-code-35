# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


import unittest

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from pyspark import SparkContext, SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
from pyspark.sql.types import StructType, DoubleType, StringType, ArrayType

from preparation_and_cleaning import *


@unittest.skipIf("ICP" in get_env(), "skipped on ICP")
class TestAIOpenScaleClient(unittest.TestCase):
    binding_uid = None
    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    subscription = None
    subscription_uid = None
    test_uid = str(uuid.uuid4())
    model_name = None
    deployment_name = None

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = self.ai_client.data_mart.get_details()
        print("Datamart details: {}".format(details))
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_04_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))
        self.assertIsNotNone(self.binding_uid)

    def test_05_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        print("Binding id: {}".format(binding_uid))
        self.assertEqual(binding_uid, TestAIOpenScaleClient.binding_uid)

        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(
            binding_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.wml_client)

    def test_06_list_instances(self):
        self.ai_client.data_mart.bindings.list()

    def test_07_get_binding_uid(self):
        print("Bindings list:\n")
        self.ai_client.data_mart.bindings.list()
        binding_uid = self.ai_client.data_mart.bindings.get_uids()[0]
        print("Datamart details binding guid: {}".format(binding_uid))
        self.assertIsNotNone(binding_uid)
        self.assertEqual(binding_uid, self.binding_uid)

    def test_08_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_09_prepare_deployment(self):
        asset_name = "AIOS Spark German Risk model"
        deployment_name = "AIOS Spark German Risk deployment"

        TestAIOpenScaleClient.model_name = asset_name
        TestAIOpenScaleClient.deployment_name = deployment_name

        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        spark_df = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ",").option(
            "inferSchema", "true").load(
            os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))
        spark_df.printSchema()

        (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
        print("Number of records for training: " + str(train_data.count()))
        print("Number of records for evaluation: " + str(test_data.count()))

        si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
        si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
        si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
        si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
        si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
        si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
        si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
        si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
        si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
        si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
        si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
        si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
        si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
        si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
        label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

        va_features = VectorAssembler(
            inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                       "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX", "InstallmentPlans_IX",
                       "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                       "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age", "ExistingCreditsCount",
                       "Dependents"], outputCol="features")

        classifier = RandomForestClassifier(featuresCol="features")

        pipeline = Pipeline(
            stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings, si_ForeignWorker,
                    si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                    si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

        model = pipeline.fit(train_data)
        predictions = model.transform(test_data)
        evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
        auc = evaluator.evaluate(predictions)

        print("Accuracy = %g" % auc)

        train_data_schema = spark_df.schema
        label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
        label_field.metadata['values'] = si_Label.labels
        input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

        output_data_schema = StructType(list(input_fileds)). \
            add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
            add("predictedLabel", StringType(), True,
                {'modeling_role': 'decoded-target', 'values': si_Label.labels}). \
            add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

        model_props = {
            self.wml_client.repository.ModelMetaNames.NAME: "{}".format(asset_name),
            self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
            self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                {
                    "name": "AUC",
                    "value": auc,
                    "threshold": 0.8
                }
            ]
        }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model, meta_props=model_props,
                                                                         training_data=train_data, pipeline=pipeline)

        print("Published model details:\n{}".format(published_model_details))
        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Deploying model: {}, deployment name: {}".format(asset_name, deployment_name))
        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name=deployment_name,
                                                        asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

        deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)
        print("Deployment details:\n{}".format(deployment_details))

    def test_10_list_subscriptions(self):
        self.ai_client.data_mart.subscriptions.list()

    def test_11_subscribe(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(self.model_uid))
        print("Subscription: {}".format(self.subscription))
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid

    def test_12_list_deployments(self):
        print("Listing deployments:\n")
        self.subscription.list_deployments()

    def test_13_get_deployments(self):
        deployments_list = self.subscription.get_deployment_uids()
        print("Deployments uids: {}".format(deployments_list))
        self.assertTrue(len(deployments_list) == 1)

    def test_14_list_and_get_uids_after_subscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list(name=self.model_name)
        subscription_uids = self.ai_client.data_mart.subscriptions.get_uids()
        self.assertTrue(len(subscription_uids) > 0)

    def test_15_prepare_deployment(self):
        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="{} 2".format(self.deployment_name), asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)
        print("New deployment uid: {}".format(self.deployment_uid))

    def test_16_update_deployments(self):
        TestAIOpenScaleClient.subscription.update()

    def test_17_check_if_deployments_were_added(self):
        deployments_list = self.subscription.get_deployment_uids()
        print("Deployments uids: {}".format(deployments_list))
        self.assertTrue(len(deployments_list) == 2)
        self.assertIn(self.deployment_uid, deployments_list)

        self.assertTrue(len(self.ai_client.data_mart.subscriptions.get_details()['subscriptions'][0]['entity']['deployments']) > 0)

    def test_18_list_models_and_functions(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()

    def test_19_get_asset_uids(self):
        asset_uids = self.ai_client.data_mart.bindings.get_asset_uids()
        print("Asset uids: {}".format(asset_uids))
        self.assertTrue(len(asset_uids) > 0)
        self.assertIn(self.model_uid, asset_uids)

    def test_20_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

    def test_21_delete_deployment(self):
        self.wml_client.deployments.delete(deployment_uid=self.deployment_uid)

    def test_22_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_23_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()

        for deployment in cls.wml_client.deployments.get_details()['resources']:
            if 'published_model' in deployment['entity'] and cls.model_uid == deployment['entity']['published_model']['guid']:
                print("Deleting deployment: {}".format(deployment['metadata']['guid']))
                cls.wml_client.deployments.delete(deployment['metadata']['guid'])
        cls.wml_client.repository.delete(cls.model_uid)
        print("Deleting model: {}".format(cls.model_uid))


if __name__ == '__main__':
    unittest.main()

### UPDATE DATABASE
# @unittest.skip("Rework needed")
# class TestAIOpenScaleClient(unittest.TestCase):
#     binding_uid = None
#     deployment_uid = None
#     model_uid = None
#     aios_model_uid = None
#     scoring_url = None
#     labels = None
#     logger = logging.getLogger(__name__)
#     ai_client = None
#     wml_client = None
#     subscription = None
#     test_uid = str(uuid.uuid4())
#
#     model = GoSales()
#
#     @classmethod
#     def setUpClass(self):
#
#         clean_env()
#
#         self.aios_credentials = get_aios_credentials()
#         self.wml_credentials = get_wml_credentials()
#         self.postgres_credentials = get_postgres_credentials()
#         self.db2_credentials = get_db2_datamart_credentials()
#         self.postgres_schema = get_schema_name()
#         self.db2_schema = get_db2_schema_name()
#
#         clean_db2_schema(self.db2_credentials, self.db2_schema)
#
#     def test_01_create_client(self):
#         TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)
#         self.assertIsNotNone(TestAIOpenScaleClient.ai_client)
#
#     def test_02_setup_data_mart(self):
#         TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=self.postgres_schema)
#
#     def test_03_bind_wml_instance(self):
#         TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))
#         self.assertIsNotNone(TestAIOpenScaleClient.binding_uid)
#
#     def test_04_get_wml_client(self):
#         binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
#         print("Binding id: {}".format(binding_uid))
#         self.assertEqual(binding_uid, TestAIOpenScaleClient.binding_uid)
#
#         TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)
#         self.assertIsNotNone(TestAIOpenScaleClient.wml_client)
#
#     def test_05_prepare_deployment(self):
#         published_model = self.model.publish_to_wml(self.wml_client)
#         print("Published model: {}".format(published_model))
#         self.assertIsNotNone(published_model)
#
#         TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model)
#         print("Published model uid: {}".format(TestAIOpenScaleClient.model_uid))
#
#         deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
#                                                         asynchronous=False)
#         print("Deployment: {}".format(deployment))
#         self.assertIsNotNone(deployment)
#         TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)
#         print("Deployment uid: {}".format(TestAIOpenScaleClient.deployment_uid))
#
#     def test_06_subscribe(self):
#         subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid, input_data_type='structured'))
#         TestAIOpenScaleClient.aios_model_uid = subscription.uid
#         print('XXX ' + str(subscription.get_details()))
#         self.assertTrue('structured' in str(subscription.get_details()))
#
#     def test_07_select_asset_and_get_details(self):
#         TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.aios_model_uid)
#         print('Subscription details: ' + str(TestAIOpenScaleClient.subscription.get_details()))
#
#     def test_07b_list_deployments(self):
#         TestAIOpenScaleClient.subscription.list_deployments()
#
#     def test_08_setup_payload_logging(self):
#         TestAIOpenScaleClient.subscription.payload_logging.enable()
#
#     def test_09_get_payload_logging_details(self):
#         payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
#         print(str(payload_logging_details))
#
#     def test_10_score(self):
#         deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
#         scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)
#
#         payload_scoring = self.model.get_scoring_payload()
#
#         for i in range(0, 5):
#             scorings = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
#             self.assertIsNotNone(scorings)
#
#         import time
#         print("Waiting 1 minute for propagation.")
#         time.sleep(60)
#
#     def test_11_stats_on_payload_logging_table(self):
#         TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
#         TestAIOpenScaleClient.subscription.payload_logging.show_table()
#         TestAIOpenScaleClient.subscription.payload_logging.describe_table()
#         pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
#         print(str(pandas_df))
#         self.assertTrue(pandas_df.size > 1)
#
#     def test_12_disable_payload_logging(self):
#         TestAIOpenScaleClient.subscription.payload_logging.disable()
#
#     def test_13_get_metrics(self):
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))
#
#     def test_14_unsubscribe(self):
#         TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
#
#     def test_15_unbind(self):
#         TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
#
#     def test_16_update_datamart(self):
#         TestAIOpenScaleClient.ai_client.data_mart.update(db_credentials=self.db2_credentials, schema=self.db2_schema)
#
#     def test_17_bind_wml_instance(self):
#         TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))
#         self.assertIsNotNone(TestAIOpenScaleClient.binding_uid)
#
#     def test_18_subscribe(self):
#         subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
#         TestAIOpenScaleClient.aios_model_uid = subscription.uid
#
#     def test_19_select_asset_and_get_details(self):
#         TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.aios_model_uid)
#         print('Subscription details: ' + str(TestAIOpenScaleClient.subscription.get_details()))
#
#     def test_20_list_deployments(self):
#         TestAIOpenScaleClient.subscription.list_deployments()
#
#     def test_21_setup_payload_logging(self):
#         TestAIOpenScaleClient.subscription.payload_logging.enable()
#
#     def test_22_get_payload_logging_details(self):
#         payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
#         print(str(payload_logging_details))
#
#     def test_23_score(self):
#
#         deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
#         scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)
#
#         payload_scoring = self.model.get_scoring_payload()
#
#         for i in range(0, 5):
#             scorings = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
#             self.assertIsNotNone(scorings)
#
#         import time
#         print("Waiting 1 minute for propagation.")
#         time.sleep(60)
#
#     def test_24a_stats_on_payload_table_from_db2(self):
#         tables = list_db2_tables(self.db2_credentials, self.db2_schema)
#         payload_table = None
#         for table in tables:
#             if "Payload" in table:
#                 payload_table = table
#
#         self.assertIsNotNone(payload_table)
#         print("Payload table: {}".format(payload_table))
#         table_content = execute_sql_query(""" SELECT * FROM "{}" """.format(payload_table), db2_credentials=self.db2_credentials)
#         print(table_content)
#
#         self.assertEqual(len(table_content), 10)
#
#     def test_24b_stats_on_payload_logging_table(self):
#         TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
#         TestAIOpenScaleClient.subscription.payload_logging.show_table()
#         TestAIOpenScaleClient.subscription.payload_logging.describe_table()
#         pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
#         print(str(pandas_df))
#         self.assertTrue(pandas_df.size > 1)
#
#     def test_25_disable_payload_logging(self):
#         TestAIOpenScaleClient.subscription.payload_logging.disable()
#
#     def test_26_get_metrics(self):
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
#         print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))
#
#     def test_27_unsubscribe(self):
#         TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
#
#     def test_28_clean(self):
#         self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
#         self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)
#
#     def test_29_unbind(self):
#         TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
#
#     def test_30_delete_data_mart(self):
#         TestAIOpenScaleClient.ai_client.data_mart.delete()
#
#
# if __name__ == '__main__':
#     unittest.main()
