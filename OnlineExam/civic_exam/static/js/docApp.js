var docApp = angular.module('docApp', []);

docApp.controller('tsearch', function ($scope, $sce, $http) {
    $scope.cronstatus = '\<span style="color:red"> Cannot locate the cron status file!<span>';
    $http.get('cronjob/')
        .success(function (data, status) {
            if (data && status === 200) {
                $scope.cronstatus = data.replace(/(?:\r\n|\r|\n)/g, '<br>');
                //console.log($scope.cronstatus);
            }
        });
    //$http.get('logReader.jsp')
    $http.get('logReader/')
        .success(function (data, status) {
            if (data && status === 200) {
                $scope.jobstatus = data;
                //console.log($scope.jobstatus);
            }
        });
    $scope.highlight = function (text, search) {
        if (!search || search.match(/^([<>br]|br)$/i)) {
            return $sce.trustAsHtml(text);
        }
        return $sce.trustAsHtml(text.replace(new RegExp(search, 'gi'), '<span class="highlightedText">$&</span>'));
    };
});

docApp.controller('rotable', function ($scope, $sce, $http) {
    $http.get('csvReader/')
        .success(function (data, status) {
            if (data && status === 200) {
                $scope.csvdata = data;
                //console.log($scope.csvdata);
            }
        });
});

docApp.controller('urlparam', function ($scope, $location) {
    var qs = $location.search();
    if(qs['viewpage']){
        $scope.subPage = qs['viewpage']+'.htm';
        //$location.search('viewpage','tt');
    }
    if(qs['fold']){
        angular.element('#menu-toggle').trigger('click');
    }
    //console.log($scope.subPage); // debug
});

//docApp.controller('n3lc', function ($scope, $sce, $http) {
//
//    // get plot data for n3-line-chart NC plot
//    $http.get('csvReader/?csvfile=nc_stats.csv&n3lc=1').then(function(res){
//        $scope.plotdata_nc = res.data;
//    });
//
//    // for new customer
//    $scope.opns_nc = {
//        drawDots: false,
//        axes:{
//            x: {key:"Date", type:"date", // zoomable:"true",
//                ticksFormat:"%Y"}
//        },
//        series: [ // Unique_Email_NC	Unique_Persona_Exact_NC	Unique_Household_Exact_NC
//            {y: "Unique_Email_NC", label: "Unique_Email_NC", color: "#9467bd", thickness: "3px"},
//            {y: "Unique_Persona_Exact_NC", label: "Unique_Persona_Exact_NC", color: "#d62728", thickness: "3px"},
//            {y: "Unique_Household_Exact_NC", label: "Unique_Household_Exact_NC", color: "#17becf", thickness: "3px"},
//        ],
//        tooltip: {
//            mode: 'scrubber', formatter: function(x, y, series) {
//                return d3.time.format("%b/%y")(new Date(x))+': '+d3.format(',')(y);
//            }
//        }
//    };
//
//    // for cumulative new customer
//    $scope.opns_nc_cum = {
//        drawDots: false,
//        axes:{
//            x: {key:"Date", type:"date", //zoomable:"true", //tooltipFormat:"%Y%m",
//                ticksFormat:"%Y"},
//            y: {ticksFormat:""}
//        },
//        series: [ // Unique_Email_Cum	Unique_Persona_Exact_Cum	Unique_Household_Exact_Cum
//            {y: "Unique_Email_Cum", label: "Unique_Email_Cum", color: "#9467bd", thickness: "3px"},
//            {y: "Unique_Persona_Exact_Cum", label: "Unique_Persona_Exact_Cum", color: "#d62728", thickness: "3px"},
//            {y: "Unique_Household_Exact_Cum", label: "Unique_Household_Exact_Cum", color: "#17becf", thickness: "3px"},
//        ],
//        tooltip: {
//            mode: 'scrubber', formatter: function(x, y, series) {
//                return d3.time.format("%b/%y")(new Date(x))+': '+d3.format(',')(y);
//            }
//        }
//    };
//
//    // get plot data for n3-line-chart NC plot
//    $http.get('csvReader/?csvfile=ac_stats.csv&n3lc=1').then(function(res){
//        $scope.plotdata_ac = res.data;
//    });
//
//    // for active customer
//    $scope.opns_ac = {
//        drawDots: false,
//        axes:{
//            x: {key:"Date", type:"date", // zoomable:"true",
//                ticksFormat:"%Y"}
//        },
//        series: [ // UniqueAC_Email	UniqueAC_Persona	UniqueAC_Household
//            {y: "UniqueAC_Email", label: "UniqueAC_Email", color: "#9467bd", thickness: "3px"},
//            {y: "UniqueAC_Household", label: "UniqueAC_Household", color: "#d62728", thickness: "3px"},
//            {y: "UniqueAC_Persona", label: "UniqueAC_Persona", color: "#17becf", thickness: "3px"},
//        ],
//        tooltip: {
//            mode: 'scrubber', formatter: function(x, y, series) {
//                return d3.time.format("%b/%y")(new Date(x))+': '+d3.format(',')(y);
//            }
//        }
//    };
//
//});
