from unittest import TestCase
import uuid

from test.unit.client import Client


class TestProcess(TestCase):
    def setUp(self):
        super(TestProcess, self).setUp()
        self.client = Client()

    def test_payer_list(self):
        response = self.client.get('/source-system/payer/')
        self.assertEqual(response.status_code, 200)

    def test_product_list(self):
        response = self.client.get('/source-system/product/')
        self.assertEqual(response.status_code, 200)

    def test_payer_source_system_list(self):
        params = {'source_system_name': "manual_insert"}

        response = self.client.get('/source-system/', params=params)
        self.assertEqual(response.status_code, 200)

    def test_product_feature_create_existing_product(self):
        randomstring = str(uuid.uuid4())
        send_data = {"master_feature": randomstring, "feature": randomstring, "product": "test_product"}

        response = self.client.post('/source-system/product-feature/', json=send_data)
        self.assertEqual(response.status_code, 201)

    def test_product_feature_create_new_product(self):
        randomstring = str(uuid.uuid4())
        send_data = {"master_feature": randomstring, "feature": randomstring, "product": randomstring}

        response = self.client.post('/source-system/product-feature/', json=send_data)
        self.assertEqual(response.status_code, 201)

    def test_product_feature_create_bad_request_no_product(self):
        randomstring = str(uuid.uuid4())
        send_data = {"master_feature": randomstring, "feature": randomstring}

        response = self.client.post('/source-system/product-feature/', json=send_data)
        self.assertEqual(response.status_code, 400)

    def test_product_feature_list(self):
        params = {'source_system_name': "manual_insert"}

        response = self.client.get('/source-system/product-feature/', params=params)
        self.assertEqual(response.status_code, 200)

    def test_payer_source_system_create(self):
        randomstring = str(uuid.uuid4())
        send_data = {"source_system_name": randomstring, "payer": "test_payer", "product": "test_product"}

        response = self.client.post('/source-system/', json=send_data)
        self.assertEqual(response.status_code, 201)

    def test_payer_source_system_create_no_product_no_payer(self):
        randomstring = str(uuid.uuid4())
        send_data = {"source_system_name": randomstring}

        response = self.client.post('/source-system/', json=send_data)
        self.assertEqual(response.status_code, 201)
