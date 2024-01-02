import unittest
import json
from rest_framework.test import APIClient
import environ
env = environ.Env()
environ.Env.read_env(".env")
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse

ERRORS ={
    "required_field":"This field is required."
}


class JwtAuthTokenTest(unittest.TestCase):
    login_url="/auth/api/login"
    json_content_type="application/json"

    def setUp(self):
        
        self.client= APIClient()
        self.correct_user=env('CORRECT_USER')
        self.correct_passwd=env('CORRECT_PASSWD')
        self.incorrect_user=env('INCORRECT_USER')
        self.incorrect_passwd=env('INCORRECT_PASSWD')
        self.valid_user = {"username":self.correct_user,"password":self.correct_passwd}
        self.invalid_user={"username":self.incorrect_user,"password":self.incorrect_passwd}
        self.invalid_cred_data={"username":self.incorrect_user,"pass":self.incorrect_passwd}
        self.expired_token=""
        self.invalid_token=""
        self.refresh_token=""
        self.valid_token ="++"
        self.successlogin_resp_format ={ "refresh":"","access":""}
        self.invalid_user_resp={"detail":"No active account found with the given credentials"}
        self.invalid_cred_data_resp={"username":[ERRORS['required_field']],"password":[ERRORS['required_field']]}
        self.getauthtoken()
        self.false_token="Bearer  asdasdaasdasidasdashdhasdhasdnashdhas"

    
    
    def test_invaliduserlogin(self):
        resp = self.client.post(self.login_url, json.dumps(self.invalid_user),content_type=self.json_content_type)
        jsonresp= resp.json()
        self.assertEqual(resp.status_code ,401)
        self.assertEqual(jsonresp , self.invalid_user_resp)
    
    def test_invalid_cred_data(self):
        resp = self.client.post(self.login_url, data=self.invalid_cred_data)
        jsonresp = resp.json()
        self.assertEqual(resp.status_code, 400)
        self.assertIn(ERRORS["required_field"],list(jsonresp.values())[0])


    def getauthtoken(self):
        resp = self.client.post(self.login_url,json.dumps(self.valid_user),content_type=self.json_content_type)
        jsonresp= resp.json()
        self.valid_token=jsonresp["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  {self.valid_token}")
        self.refresh_token = jsonresp["refresh"]

    def test_validtoken(self):
        resp = self.client.post("/auth/api/authenticated_testview")
       
        self.assertEqual(resp.status_code,200)

    def test_refreshtoken(self):
        resp = self.client.post("/auth/api/token/refresh/", data=json.dumps({"refresh":self.refresh_token}), content_type=self.json_content_type)
        jsonresp = resp.json()
        self.assertIn("access", jsonresp)
        self.assertEqual(resp.status_code,200)
        

    def test_invalidtoken(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.false_token)
        resp = self.client.post("/auth/api/authenticated_testview")
        
        self.assertEqual(resp.status_code,401)


    def test_validuserlogin(self):
        resp = self.client.post("/auth/api/login",json.dumps(self.valid_user),content_type=self.json_content_type)
        jsonresp= resp.json()
        self.valid_token=jsonresp["access"]
        
        self.assertEqual(jsonresp.keys(),self.successlogin_resp_format.keys())



class TestChangePassword(unittest.TestCase):
    url=reverse('change_password')
    login_url="/auth/api/login"
    json_content_type="application/json"

    def setUp(self):
        self.client= APIClient()
        self.correct_user=env('CORRECT_USER')
        self.valid_token=""
        self.correct_passwd=env('CORRECT_PASSWD')
        self.valid_user = {"username":self.correct_user,"password":self.correct_passwd}
        self.correct_password_data={"password":'1234', "password2":'1234'}
        self.mismatch_password_data={"password":'12345', "password2":'123'}
        self.no_password_data={}
        self.invalid_password_data={"password":"1234","pass":"1234"}
        self.false_token="Bearer  asdasdaasdasidasdashdhasdhasdnashdhas"
        self.invalid_cred_data_resp={"password": [ERRORS['required_field']],"password2": [ERRORS['required_field']]
}

    def authenticate(self):
        '''user authentication'''
        res = self.client.post(self.login_url, json.dumps(self.valid_user), content_type=self.json_content_type)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.json()['access']}")


    def test_authenticated_user_password_match(self):

        self.authenticate()
        res = self.client.post(self.url,json.dumps(self.correct_password_data), content_type=self.json_content_type )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["msg"], 'Password Changed Successfully')


    def test_not_authenticated(self):

        res = self.client.post(self.url,json.dumps(self.correct_password_data), content_type=self.json_content_type )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_invalid_token(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.false_token)
        res = self.client.post(self.url,json.dumps(self.correct_password_data), content_type=self.json_content_type )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_authenticated_user_password_mismatch(self):

        self.authenticate()
        res = self.client.post(self.url,json.dumps(self.mismatch_password_data), content_type=self.json_content_type )
        self.assertEqual(res.status_code, 400)
        self.assertIn("non_field_errors", res.json())

        
    def test_authenticated_user_with_invalid_password_data(self):

        self.authenticate()
        res = self.client.post(self.url,json.dumps(self.invalid_password_data), content_type=self.json_content_type )
        jsonresp = res.json()
        self.assertEqual(res.status_code, 400)
        self.assertIn(ERRORS["required_field"],list(jsonresp.values())[0])
        

    def test_authenticated_user_with_no_data(self):

        self.authenticate()
        res = self.client.post(self.url,json.dumps(self.no_password_data), content_type=self.json_content_type )
        jsonresp = res.json()
        self.assertEqual(res.status_code, 400)
        self.assertIn(ERRORS["required_field"],list(jsonresp.values())[0])





