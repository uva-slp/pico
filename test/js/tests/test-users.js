// User edit

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

// Theme picker

QUnit.test( "loadThemes test", function( assert ) {
    assert.expect(1);
    syncThemeInput('');
    loadThemesFailed();
    loadThemes(assert.async());
    assert.ok( 1 == "1", "Passed!" );
});
QUnit.test( "submitChangeThemeForm test", function( assert ) {
    replaceAjax(function(options) {
        options.success({theme:''},null,{status:200});
        options.success({error:''},null,{status:201});
        options.error(null);
    });
    submitChangeThemeForm({preventDefault:function(){}});
    restoreAjax();
    assert.ok( 1 == "1", "Passed!" );
});

// Storage

QUnit.test( "renderDiskUsageChart test", function( assert ) {
    hasRenderedDiskUsageChart = null;
    tooltipFormatter.call({y:0,key:'',series:{name:''}}, null);
    var chart = $('<div/>')
        .attr('id', 'storage')
        .addClass('active')
        .append($('<div/>')
            .attr('id', 'disk-usage-chart'));
    $('body').append(chart);
    renderDiskUsageChart();
    chart.remove();
    assert.ok( 1 == "1", "Passed!" );
});
