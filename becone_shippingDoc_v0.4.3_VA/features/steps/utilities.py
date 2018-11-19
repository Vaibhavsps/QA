
from delayedAssert import expect, assert_expectations


def verify_tag_existance(item_dict, table,column_header):
    for row in table:
        expect(row[0] in item_dict.keys(),'Expected value:"%s" was not found in:%s' % (row[0], item_dict.keys()))
    assert_expectations()


# Not in use
def removeTag(ZPL, tag_to_remove):
    final_zpl = ZPL
    return final_zpl



#@then ('we save the value of "id" in "{varName}"')
#def step_impl(context,varName):
#    setattr(context,varName,id)


#then ('abc "{varName}"')the output should contain "templates" array with "1" recrod having "ID" as "{varName}"
#def step_impl(context,varName):
#    print(varName[6:])
#    abc=getattr(context, varName[6:])
#    print(abc)
#    assert False
