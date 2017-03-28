QUnit.module("toggleTester", {
    setup: function () {
        $("#qunit").append('<input class="" id="id_autojudge_enabled" name="autojudge_enabled" type="checkbox"> ');
        $("#qunit").append('<select class="form-control" disabled="disabled" id="id_autojudge_review" name="autojudge_review" title="">' +
            '<option value="1">Manual review incorrect submissions</option>' +
            '<option value="2">Manual review all submissions</option></select> ');
    }
});

var is_unchecked = true;

function autojudgeCheckboxToggle() {
    if(is_unchecked == true) {
        is_unchecked = false;
        toggleTest();
        //$("#id_autojudge_enabled").click();
    } else {
        is_unchecked = true;
        toggleTest();
    }
    /*if ($("#id_autojudge_enabled").is(":checked")) {
        is_unchecked = true;
    } else {
        is_unchecked = false;
        $("#EmailRequirementSatisfied").val("");
    }*/
}

QUnit.test("toggleTest()", function (assert) {
    //$("#id_autojudge_enabled").val("test value");
    /*
        document.getElementById('IsOtherEmail').checked=true;
        $("#IsOtherEmail").prop("checked", true);
        $("#IsOtherEmail").attr("checked", "checked");
        $("#IsOtherEmail").val(true);
    */

    //$("#id_autojudge_enabled").trigger("click");
    assert.ok(is_unchecked == true, "The checkbox was initially checked");
    //assert.ok($("#id_autojudge_enabled").prop('checked') == false, "The checkbox should initially be unchecked");
    //assert.ok($("#id_autojudge_review").prop('disabled') == true, "The autojudge review should initially be disabled");
    //assert.ok(is_unchecked == "true", "The checkbox should initially be unchecked");
    //autojudgeCheckboxToggle();
    autojudgeCheckboxToggle();

    //$("#id_autojudge_enabled").checked = true;
    //$("#id_autojudge_enabled").click();
    //$('#id_autojudge_review').prop('disabled', false);

    //$("#id_autojudge_enabled").prop("checked", true);
    //autojudgeCheckboxLock();
    assert.ok(is_unchecked == false, "The checkbox was not successfully marked check");
    //assert.ok($("#id_autojudge_enabled").prop('checked') == true, "The checkbox was not successfully marked check");
    //assert.ok($("#id_autojudge_review").prop('disabled') == false, "The autojudge review was not successfully enabled");

    autojudgeCheckboxToggle();
    assert.ok(is_unchecked == true, "The checkbox isn't back to unchecked");
});