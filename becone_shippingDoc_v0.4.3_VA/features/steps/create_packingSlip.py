from behave import *
import requests
import jpath
import json
import simplejson
import nose
from delayedAssert import expect, assert_expectations
import uuid



#we provide unique value to "template_name"
@given('we provide unique value to "{value_toSearch}"')
def step_impl(context,value_toSearch):
    #print ("<"+value_toSearch+">")
    context.testData_jsonBody=context.testData_jsonBody.replace("<"+value_toSearch+">",str(uuid.uuid1()))
    #print(context.testData_jsonBody)
    pass

