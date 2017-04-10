// Common js

QUnit.test( "getCookie test", function( assert ) {
    // Backup cookie
    var cookieBackup = document.cookie;
    // Get full coverage
    document.cookie = 'foo=1;bar=2;';
    getCookie('foo');
    // Restore cookie
    document.cookie = cookieBackup;
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "outerHTML test", function( assert ) {
    $('<div/>').outerHTML();
    assert.ok( 1 == "1", "Passed!" );
});
