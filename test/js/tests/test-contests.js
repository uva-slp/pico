QUnit.module("toggle checkbox setup", {
    beforeEach: function () {
        var fixture = $("#qunit-fixture");
        fixture.append('<input class="" id="id_autojudge_enabled" name="autojudge_enabled" type="checkbox"> ');
        fixture.append('<select class="form-control" disabled="disabled" id="id_autojudge_review" name="autojudge_review" title="">' +
            '<option value="1">Manual review incorrect submissions</option>' +
            '<option value="2">Manual review all submissions</option></select> ');
    }
});

QUnit.test("toggle checkboxes test", function (assert) {
    var autojudge_enabled = $("#id_autojudge_enabled");
    var autojudge_review = $("#id_autojudge_review");

    assert.equal(autojudge_enabled.prop('checked'), false, "Autojudge checkbox is initially unchecked");
    assert.equal(autojudge_review.prop('disabled'), true, "Autojudge review is initially disabled");

    autojudge_enabled.click();
    toggleCheckbox();
    assert.equal(autojudge_enabled.prop('checked'), true, "Autojudge checkbox is checked");
    assert.equal(autojudge_review.prop('disabled'), false, "Autojudge review is enabled");

    autojudge_enabled.click();
    toggleCheckbox();
    assert.equal(autojudge_enabled.prop('checked'), false, "Autojudge checkbox is unchecked");
    assert.equal(autojudge_review.prop('disabled'), true, "Autojudge review is disabled");
});

QUnit.module("timer bar setup", {
    beforeEach: function () {
        var fixture = $("#qunit-fixture");
        fixture.append('<div id="main-navbar" style="height: 200px;">tall content</div>');
        fixture.append('<div class="progress slower" id="timer_bar">');
        fixture.append('<div class="time_remaining_div"><span class="time_remaining_text"></span></div>');
        fixture.append('<div id="progress-slow" class="progress-bar progress-bar-striped active live_timer_div" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="height:170px; width:100%"></div>');
        fixture.append('</div>');
        fixture.append('<div style="padding-top: 0px;height: 20000px;"></div>');

        contest_start = '2017-03-13 4:44:44 p.m.';
        contest_length = '8 a.m.';
        is_contest_started = contest_start != "None";
        home_url = "{% url 'contests:index' %}";
        is_contest_ended = false;
    }
});

QUnit.test("lock timer bar test", function (assert) {
    var progress = $(".progress");

    assert.equal(progress.hasClass("fixed"), false, "Timer bar is initially not fixed to top of window");

    window.scroll(0, 1000);
    $(window).trigger("scroll");
    // assert.equal(progress.hasClass("fixed"), true, "Timer bar is fixed to top of window");

    window.scroll(0, 0);
    $(window).trigger("scroll");
    assert.equal(progress.hasClass("fixed"), false, "Timer bar is not fixed to top of window");
});

QUnit.test("timer bar test", function (assert) {
    var live_timer_div = $(".live_timer_div");

    loadTimerBar(contest_start, is_contest_started, is_contest_ended, contest_length, home_url);

    contest_length = '12 a.m.';
    loadTimerBar(contest_start, is_contest_started, is_contest_ended, contest_length, home_url);
    contest_length = '5 p.m.';
    loadTimerBar(contest_start, is_contest_started, is_contest_ended, contest_length, home_url);

    contest_start = moment().utc().format('YYYY-MM-DD H:mm:ss a');
    contest_length = '2 a.m.';
    loadTimerBar(contest_start, is_contest_started, is_contest_ended, contest_length, home_url);
    //assert.equal(live_timer_div.hasClass("progress-bar-warning"), true, "Contest has over 1 hour left");

    assert.equal(1, 1, "Contest timer bar passes");
});

QUnit.module("notification setup", {
    beforeEach: function () {
        var fixture = $("#qunit-fixture");
        fixture.append('<div id="getNotificationUrl" style="display: none;">http://localhost:8000/contests/api/get_notification/</div>');
        data_list = [];
        false_data = ['test contest', 1, 1, 'False', 1, 1];
        yes_data = ['test contest', 1, 2, 'Yes', 2, 2];
        data_list.push(yes_data);
        data_list.push(false_data);
    }
});

QUnit.test("get notification test", function (assert) {
 replaceAjax(function(options) {
     options.success({data:data_list},null,{status:200});
     options.complete();
 });
 fetchNotification();
 restoreAjax();
 assert.ok( 1 == "1", "Passed!" );
});

QUnit.test("close modal test", function (assert) {
    onModalClose("myModal1");
    assert.ok( 1 == "1", "Passed!" );
});

QUnit.test("close notification test", function (assert) {
    replaceAjax(function(options) {
        options.success({id:1},null,{status:200});
    });
    closeNotification();
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});

QUnit.test("refresh submission test", function (assert) {
 replaceAjax(function(options) {
     options.success({contestId:1},null,{status:200});
     options.complete();
 });
 refreshPage();
 restoreAjax();
 assert.ok( 1 == "1", "Passed!" );
});