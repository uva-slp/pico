var hasRenderedDiskUsageChart = null;
function renderDiskUsageChart() {
    if ($('#storage').hasClass('active') && hasRenderedDiskUsageChart === null) {
        var myChart = Highcharts.chart('disk-usage-chart', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Disk Usage'
            },
            tooltip: {
                shared: true,
                formatter: function() {
                    var size = this.y;
                    var unit = 'B';
                    if (size >= 1024) { size/=1024; unit='KB'}
                    if (size >= 1024) { size/=1024; unit='MB'}
                    if (size >= 1024) { size/=1024; unit='GB'}
                    if (size >= 1024) { size/=1024; unit='TB'}
                    size = size.toFixed(1);
                    return '<span style="font-size: 10px">' + this.key + '</span><br/>' +
                        this.series.name + ': <b>'+ size +' ' + unit + '</b>';
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                name: 'Disk Usage',
                colorByPoint: true,
                data: [{
                    name: 'PiCO',
                    y: parseInt($('#disk-usage > #pico').text())
                }, {
                    name: 'Database',
                    y: parseInt($('#disk-usage > #db').text())
                }, {
                    name: 'Other',
                    y: parseInt($('#disk-usage > #other').text())
                }, {
                    name: 'Available',
                    y: parseInt($('#disk-usage > #free').text())
                }]
            }]
        });

        hasRenderedDiskUsageChart = true;
    }
}
renderDiskUsageChart();
$('a[data-toggle="pill"][href="#storage"]').on('shown.bs.tab', function (e) {
    renderDiskUsageChart();
});