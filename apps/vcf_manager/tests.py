from os import access
from django.test import TestCase

import json
from rest_framework.test import APIClient
from rest_framework import response, status

from apps.vcf_manager.utils import utils

class VcfManagerTestCase(TestCase):


    def setUp(self):

  
        self.access_token= utils.get_token()
        self.access_token_bad='9944b09199c62bcf9418ad846dd'

        self.variant = { "CHROM": "chr1","POS":1000,"ALT":"A","REF":"G","ID":"rs565464"}
        self.variant_miss_alt = { "CHROM": "chr1","POS":1000,"ALT":"","REF":"G","ID":"rs565464"}
        self.variant_bad_id = { "CHROM": "chr1","POS":1000,"ALT":"","REF":"G","ID":"r565464"}


    def test_new_variant(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        response = client.post(
            '/api/add-new-variant/',
            self.variant,
            format='json'
            )
        response_missing_alt = client.post(
            '/api/add-new-variant/',
            self.variant_miss_alt,
            format='json'
            )
        response_bad_id = client.post(
            '/api/add-new-variant/',
            self.variant_bad_id,
            format='json'
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_missing_alt.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_bad_id.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_variant_bad_token(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token_bad)

        response = client.post(
            '/api/add-new-variant/',
            self.variant,
            format='json'
            )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_AUTHORIZATION(self):

        client = APIClient()

        response = client.post(
            '/api/add-new-variant/',
            self.variant,
            format='json'
            )
       

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_variant_by_id(self):

        client = APIClient()
        
        response = client.get(
            '/api/rs62635284',
            )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_variant_not_found(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        
        response = client.get(
            '/api/rs6263528499',
            )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_http_accept(self):

        client = APIClient() 
        
        response = client.get(
            '/api/',
            HTTP_ACCEPT='application/javascript'
            )

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)





