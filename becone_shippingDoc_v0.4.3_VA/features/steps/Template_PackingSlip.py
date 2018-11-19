from behave import *
import requests
import jpath
import json
import simplejson
import nose
from delayedAssert import expect, assert_expectations
from features.steps.utilities import *

def test_should_pass():
    expect(1 == 1, 'one is one')
    assert_expectations()

def test_should_fail():
    expect(1 == 2)
    x = 1
    y = 2
    expect(x == y, 'x:%s y:%s' % (x, y))
    expect(1 == 1)
    assert_expectations()


#to read a file and return the content
def loadfile(path):
    with open(path, 'r') as f:
        data = f.read()
    return data

#Given load test data from "#DR#.createTemplate_PackingSlip_sample"
@Given('load test data from "{fileName}"')
def step_impl(context,fileName):
    data =loadfile('features/testData/'+fileName[5:])
    #context.zpl_json = json.loads(json.dumps(data))
    #value= loadfile('features/testData/create.json')
    #my_bytes = value.encode("utf-8")
    #decoded_value = my_bytes.decode("unicode_escape")
    context.testData_jsonBody = data
    pass


@given('set base url to "{base_URL}"')
def step_impl(context, base_URL):
    context.base_url= base_URL
    pass


@when('we do "{request_verb}" request to URL "{path}"')
def step_impl(context, request_verb, path):
    url =context.base_url+ path

    if request_verb.lower() == "get":
        context.r = getattr(requests, request_verb.lower())(url, headers="", verify=True)
    elif request_verb.lower() == "post":
        #data_json = simplejson.dumps(context.zpl_json)
        #payload = {'json_payload': data_json}
        headers = {
            'Content-Type': 'application/json',
        }
        context.r = getattr(requests, request_verb.lower())(url, headers=headers, verify=True, data=context.testData_jsonBody)
        #print (context.testData_jsonBody)


    #print(context.r.status_code)


    #raise NotImplementedError(u'STEP: When We make a  "POST" request to URL "/labels/zpl"')

# print(r.status_code)
# print(r.reason)
# print(r.headers["Content-Type"])
# print(r.json())



@then('the response status code should be equal to {expected_http_status_code}')
def step_impl(context, expected_http_status_code):
    nose.tools.assert_equal(context.r.status_code, int(expected_http_status_code))
    #raise NotImplementedError(u'STEP: Then the response status code should equal 200')


@then('the response status message should equal to "{expected_http_status_message}"')
def step_impl(context, expected_http_status_message):
    print(context.r.json)
    nose.tools.assert_equal(context.r.reason, expected_http_status_message)
    #raise NotImplementedError(u'STEP: Then the response status message should equal to "OK"')

#========================== for different assertions ====================
#expect(length_var==exp_data_array_len, 'expected value was:%d and actual value was:%d' %(exp_data_array_len, length_var))
#assert_expectations()
#assert False, "message"
#nose.tools.ok_(length_var==exp_data_array_len, 'expected value was:%d and actual value was:%d' %(exp_data_array_len, length_var))
#nose.tools.assert_equal(length_var, exp_data_array_len)
#=======================================================================

@then('the response should contain "{tag_to_find}" array of "{data_array_Length}" records')
def step_impl(context, tag_to_find, data_array_Length):

    response_json=context.r.json()
    item_dict=json.loads(json.dumps(response_json))
    length_var=len(item_dict[tag_to_find])
    exp_data_array_len=int(data_array_Length)
    nose.tools.assert_equal(length_var, exp_data_array_len)

    #expect( length_var= int(data_array_Length), "euqal"  )

    #nose.tools.assert_equal(len(item_dict[tag_to_find]),int(data_array_Length))
    #if len(item_dict[tag_to_find]) != int(data_array_Length):

        #logging.error("This is error message, 22 was not 21", False )
        #print("vaibhavccc")


    #response_json = context.r.json()
    #item_dict = jpath.get(tag_to_find, response_json)
    #nose.tools.assert_equal(len(item_dict), int(data_array_Length))


    #actual_json_value = "vaibhav-_json_value"
    #actual_json_value = jpath.get(".templates", response_json)

    #nose.tools.assert_equal(actual_json_value,"vaibhav")
    #print(actual_json_value)
    #raise NotImplementedError(u'STEP: Then the response should contain array of "20" or "less"')


@then('the "{tag_key}" should be "{expected_tag_value}"')
def step_impl(context, tag_key, expected_tag_value):

    response_json = context.r.json()
    if expected_tag_value.startswith("#DR#."):
        expected_tag_value=loadfile('features/testData/'+expected_tag_value[5:])

    # encoding and Decoding expected value to unicode for escape character
    my_bytes = expected_tag_value.encode("utf-8")
    decoded_message_expected_tag_value = my_bytes.decode("unicode_escape")

    # encoding and Decoding expected value to unicode for escape character
    actual_tag_value = jpath.get(tag_key, response_json)
    my_bytes_actual = actual_tag_value.encode("utf-8")
    decoded_message_actual_tag_value = my_bytes_actual.decode("unicode_escape")
    #print("Vaibhav agarwal - expected decoded---- " + decoded_message_expected_tag_value +"---VaiibhavEND")
    #print("Vaibhav agarwal actual--decodec ---- " + decoded_message_actual_tag_value +"---VaiibhavEND")

    #for removing max limit on comparision
    nose.tools.assert_equal.__self__.maxDiff = None
    nose.tools.assert_equal(decoded_message_actual_tag_value, decoded_message_expected_tag_value)

#all the template results should contain Description, Id, Name, Owner_Id, Owner_Name, Type of Template
@then('all the "{array_tag}" results should contain "tag"')
def step_impl(context,array_tag):
    response_json = context.r.json()
    item_dict = json.loads(json.dumps(response_json))
    item_templates=item_dict[array_tag]

    for x in item_templates:
        verify_tag_existance(x, context.table, "tag")

#Done_riya
#atleast/mimimum, atmax/maximum, exactly
@then('the output should contain "{condition}" "{expected_record_count}" record in "{tag}"')
def step_impl(context, condition, expected_record_count, tag):
    response_json = context.r.json()
    item_dict = json.loads(json.dumps(response_json))
    item_templates = item_dict[tag]

    if condition=='atleast':
        if len(item_templates)<int(expected_record_count):
            assert False, 'Expected count was:%s, and the actual was:%d' %(expected_record_count, len(item_templates))
    elif condition=='atmax':
        if len(item_templates)>int(expected_record_count):
            assert False, 'Expected count was:%s, and the actual was:%d' %(expected_record_count, len(item_templates))
    elif condition=='exactly':
        if len(item_templates)!=int(expected_record_count):
            assert False, 'Expected count was:%s, and the actual was:%d' %(expected_record_count, len(item_templates))
    else:
        assert False, "Condition did not matced with atleast/atmax/exactly"


@then('the output should contain "{column_Header}" tag')
def step_impl(context,column_Header):
    response_json = context.r.json()
    item_dict = json.loads(json.dumps(response_json))
    if column_Header.startswith("#table#."):
        verify_tag_existance(item_dict, context.table,column_Header)
    else:
        expect(column_Header in item_dict.keys(), 'Expected value:%s was not found in:%s' % (column_Header, item_dict.keys()))
        assert_expectations()



#the output should contain "templates" array with "1" recrod having "id" as "#var#.generated_ID"

@then('the output should contain "{array_tag}" array with "{result_count}" recrod having "{tag_key}" as "{value}"')
def step_impl(context,array_tag, result_count, tag_key, value):
    response_json = context.r.json()
    item_dict = json.loads(json.dumps(response_json))
    item_templates = item_dict[array_tag]
    #jpath.get(tag_key, response_json)
    #print(item_templates)

    counter=0
    for i in item_templates:
        id_value=i[tag_key]
        if id_value==value:
            counter+=1

    nose.tools.assert_equal(int(result_count), counter)

