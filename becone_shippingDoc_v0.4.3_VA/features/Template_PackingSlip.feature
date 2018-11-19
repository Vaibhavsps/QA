Feature: Test template-packing slip file

  Background: set pre-requisite
    Given set base url to "http://localhost/templates/v1/packing-slip/template"
    #https://api.template.spsapps.net/templates/v1/lables/template"

@done
  Scenario: Test scenario to check for availability of service
    When we do "GET" request to URL "/"
    Then the response status code should be equal to 200
    And the response status message should equal to "OK"

  @done @riya_m @abcdefgh
  Scenario: test that URl "/" returns only finite results
    When we do "GET" request to URL "/"
    Then the output should contain "atmax" "10" record in "templates"

@done @riya_m
  Scenario: Test for retrieving data for a template "6ffd0165"
    When we do "GET" request to URL "/6ffd0165"
    Then the "description" should be "Packing slip"
    And the "name" should be "Wayfair LLC"
    And the "owner_name" should be "Wayfair LLC"
    And the "type" should be "packing-slip"
    And the output should contain "atleast" "2" record in "versions"

@done
  Scenario Outline: Test for retrieving data for a template "6ffd0165"
    When we do "GET" request to URL "/<template_ID>"
    Then the "description" should be "<resp_desc>"
    And the "name" should be "<resp_name>"
    And the "owner_name" should be "<resp_owner_name>"
    And the "type" should be "<resp_type>"
  Examples:
    |template_ID|resp_desc|resp_name|resp_owner_name|resp_type|
    |6ffd0165|Packing slip|Wayfair LLC|Wayfair LLC|packing-slip|
    |72876c16|I am Jacks template, I represent a pattern for which Jack describes X|Now with more formats 2|SPS Commerece|packing-slip|

  @done
  Scenario: Test scenario to check data of all templates in output
    When we do "GET" request to URL "/"
    Then the response status message should equal to "OK"
    And all the "templates" results should contain "tag"
    |tag|
    |description|
    |id         |
    |name       |
    |owner_id   |
    |owner_name |
    |type       |


  @done @smoke @fullregression
  Scenario Outline:  Test scenario to get template using template id and version
    When we do "GET" request to URL "/<template_id>/version/<version>"
    Then the response status message should equal to "OK"
    And the response status code should be equal to 200
    And the output should contain "#table#.tag" tag
    |tag|
    |created_at |
    |description|
    |id         |
    |name       |
    |owner_id   |
    |owner_name |
    |status     |
    |tags       |
    |template_data|
    |template_schema|
    And the "template_data" should be "<template_data_expected>"
    And the "template_schema" should be "<template_schema_expected>"
  Examples:
    |template_id|version|template_data_expected|template_schema_expected|
    |6ffd0165   |1      |#DR#.template_data_6ffd0165_1|#DR#.template_schema_6ffd0165_1|
    #|72876c16   |1      |#DR#.template_data_6ffd0165_1|#DR#.template_schema_6ffd0165_1|




  @negative @done
  Scenario Outline: Test scenario to get template by invalid template id
    When we do "GET" request to URL "/<template_id>"
    Then the response status message should equal to "NOT FOUND"
    And the "error.error_description" should be "Template not found"
    And the "status" should be "error"
    Examples:
      |template_id|
      |34324|
      |46485|


  @negative @done
  Scenario Outline:  Test scenario to get template by valid Template_ID and invalid version
    When we do "GET" request to URL "/<template_id>/version/<version>"
    Then the response status message should equal to "NOT FOUND"
    And the "error.error" should be "not_found"
    And the "error.error_description" should be "Template version not found"
    Examples:
      |template_id|version|
       |6ffd0165   |5      |

  @negative @done

  Scenario Outline:  Test scenario to get template by invalid Template ID and invalid version as well
    When we do "GET" request to URL "/<template_id>/version/<version>"
    Then the response status message should equal to "NOT FOUND"
    And the "error.error" should be "not_found"
    And the "error.error_description" should be "Template not found"
    Examples:
      |template_id|version|
      |5332       |5      |