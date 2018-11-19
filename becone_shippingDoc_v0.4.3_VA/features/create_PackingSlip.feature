# Created by vaibhav at 15/11/18
Feature: #Enter feature name here
  # Enter feature description here


    Background: set pre-requisite
    Given set base url to "http://localhost/templates/v1/packing-slip/template"
    #https://api.template.spsapps.net/templates/v1/lables/template"

  @done
  Scenario: Just for creation of a new template
    Given load test data from "#DR#.createTemplate_PackingSlip_sample.json"
    And we provide unique value to "template_name"
    When we do "post" request to URL "/"
    Then the response status message should equal to "CREATED"
    And the response status code should be equal to 201

  @done
  Scenario: Test scenario to create template
    Given load test data from "#DR#.createTemplate_PackingSlip_sample.json"
    And we provide unique value to "template_name"
    When we do "post" request to URL "/"
    Then the response status message should equal to "CREATED"
    And the response status code should be equal to 201
    And the output should contain "#table#.tag" tag
      |tag|
      |created_at|
      |description|
      |format     |
      |id         |
      |name       |
      |output_format|
      |owner_id     |
      |status       |
      |tags         |
      |template_data|
      |template_schema|
      |type           |
      |version        |


@wip @vaibhav_test1
 Scenario: Test scenario to get new created template
  Given load test data from "#DR#.createTemplate_PackingSlip_sample.json"
  And we provide unique value to "template_name"
  When we do "post" request to URL "/"
  Then the response status message should equal to "CREATED"
  And the response status code should be equal to 201
  #And we save the value of "id" in "generated_ID"
  When we do "GET" request to url "/"
  #Then the output should contain "templates" array with "1" recrod having "ID" as "#var#.generated_ID"
  Then the output should contain "templates" array with "1" recrod having "id" as "1296dadb"


@wip
  Scenario: To test that the templates array gets increased by 1 upon sucessfull createion of new template
    When we do "get" request to URL "/"
    Then we save the count of elements of "templates" array in "ini_Count"
    When load test data from "#DR#.createTemplate_PackingSlip_sample.json"
    And we provide unique value to "template_name"
    When we do "post" request to URL "/"
    Then the response status message should equal to "CREATED"
    And the response status code should be equal to 201
    When we do "GET" request to url "/"
   Then the response should contain "templates" array of "#var#.init_count+1" records



 Scenario: Test for retrieving data for a  new template using template_id
    When we do "GET" request to url "/<template_id>"
    Then output should contain new created template data

  Scenario: Test scenario to check version of new template created using "template_id"
     When we do "GET" request to url "/<template_id>"
     Then output should contain template of given template_id with single version 1

  Scenario: Test scenario to create template with a missing field in input json data
     When we do "POST" request to base url
     And we send "JSON" format input data with a missing field
     Then Template should not create
    And the "error.error" should be "validation_error"
    And the "status" should be "error"
    And the "error.error_description" should be "<string>"



  Scenario: Test scenario to create template with null value for a field
      When    we do "POST" request to base url
      And we send "JSON"  format input data with null value for <field>
      Then Output should show the created template with <field> null
      |field|
      |name|
      |description|
      |format     |
      |output_fromat|
      |aliases      |
      |tags         |
      |owner_id     |
      |owner_name   |
      |template_data|
      |template_scehma|