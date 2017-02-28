//Here are a couple of example tests:
QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});

QUnit.test( "getCookie test", function( assert ) {
  assert.ok( getCookie("banana") == null, "Passed!" );
});
