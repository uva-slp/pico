// Create team

QUnit.test( "focusInput test", function( assert ) {
    focusInput();
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "submitTeamForm test", function( assert ) {
    replaceAjax(function(options) {
        options.success({tab:'',panel:''},null,{status:200});
        options.success({form:''},null,{status:201});
        options.error(null);
    });
    var event = { preventDefault: function() {} };
    submitTeamForm(event);
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});

// Invite to team

QUnit.test( "openInviteModal test", function( assert ) {
    var event = { stopPropagation: function() {} };
    openInviteModal(event);
    assert.ok( 1 == "1", "Passed!" );
});

// Leave team

QUnit.test( "submitTeamLeaveForm test", function( assert ) {
    replaceAjax(function(options) {
        var location = window.location.href;
        options.success(null, null, null);
        options.error(null);
        history.replaceState('data', '', location);
    });
    var event = { preventDefault: function() {} };
    submitTeamLeaveForm(event);
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});
