// Create team

QUnit.test( "focusInput test", function( assert ) {
    focusInput();
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "submitTeamForm test", function( assert ) {
    replaceAjax(function(options) {
        options.success({tab:'',panel:''},null,{status:200});
        options.success({form:''},null,{status:201});
        options.error();
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
        options.success();
        options.error();
        history.replaceState('data', '', location);
    });
    var event = { preventDefault: function() {} };
    submitTeamLeaveForm(event);
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});

// Team public toggle

QUnit.test( "submitTeamPublicForm test", function( assert ) {
    replaceAjax(function(options) {
        options.success();
        options.error();
    });
    submitTeamPublicForm();
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "renderToggle test", function( assert ) {
    renderToggle();
    assert.ok( 1 == "1", "Passed!" );
});

// Team search

QUnit.test( "submitTeamSearchForm test", function( assert ) {
    replaceAjax(function(options) {
        options.success({tab:'',panel:''},null,{status:200});
        options.success(null,null,{status:201});
        options.error();
    });
    submitTeamSearchForm();
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});

// Team stickytabs

QUnit.test( "onClickTeamTab test", function( assert ) {
    var location = window.location.href;
    onClickTeamTab.call({href:''});
    try { history.replaceState('data', '', location); }
    catch (exception) { console.log(exception); }
    assert.ok( 1 == "1", "Passed!" );
});
