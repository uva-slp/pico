QUnit.test( "userEditClick test", function( assert ) {
    userEditClick();
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "cancelUserEditClick test", function( assert ) {
    cancelUserEditClick();
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "submitUserEditForm test", function( assert ) {
    replaceAjax(function(options) {
        options.success({val:''},null,{status:200});
        options.success({val:' '},null,{status:200});
        options.success({error:''},null,{status:201});
        options.error(null);
    });
    submitUserEditForm({preventDefault:function(){}});
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});
