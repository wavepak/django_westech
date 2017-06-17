var msReaderApp = angular.module('msReaderApp', ['n3-line-chart']);
msReaderApp.controller('msCtrl', function ($scope, $sce, $http) {
    $http.get('msReader.jsp?bronly').then(function(res){
        $scope.brands = res.data;
        //console.log($scope.brands); // debug
    });
    $http.get('msReader.jsp?hdonly').then(function(res){
        $scope.tbheaders = res.data;
        //console.log($scope.tbheaders); // debug
    });

    //one time init
    $scope.sql_brs = 'msReader.jsp';
    //console.log($scope.sql_brs); //debug
    $http.get($scope.sql_brs).then(function(res){
        $scope.tbrecs = res.data;
        //console.log($scope.tbrecs); // debug
    });

    // for n3-chars plot
    $scope.opns = {
        drawDots: true,
        axes:{
            x: {key:"date", type:"date", //zoomable:"true", tooltipFormat:"%Y%m"
                ticksFormat:"%b%y"}
            },
        series: [
            {y: "GsGM", label: "GsGM", color: "#bcbd22", thickness: "2px"},
            {y: "NetGM", label: "NetGM", color: "#17becf", thickness: "2px"},
            {y: "InvSt", label: "InvSt", color: "#9467bd", thickness: "2px"},
            {y: "SearchVol", label: "SearchVol", color: "#d62728", thickness: "2px", axis:'y2',dotSize: 2}
        ],
        tooltip: {
            mode: 'scrubber', formatter: function(x, y, series) {
                return d3.time.format("%m/%y")(new Date(x))+': '+y;
            }
        }
    };

    $scope.filterbrand = function (brs) {
        //console.log(brs); //debug
        if (brs.length>0) {
            var br_pool='(""';
            for (var i=0; i< brs.length; i++) {
                br_pool += ',"'+brs[i]+'"';
            }
            br_pool += ')';
            $scope.sql_brs = 'msReader.jsp?params=WHERE Prefix in '+ br_pool+ ' ORDER BY Brandname,yearMonth';
            //console.log($scope.sql_brs); //debug

            // Plot the first brand select
            $http.get('msReader.jsp?brgraph='+brs[0]).then(function(res){
                $scope.plotdata = res.data;
                // Set date options
                //console.log($scope.plotdata); // debug
                $scope.plotdata_org = res.data;
                $scope.br_sdt = $scope.plotdata_org[0];
                $scope.br_edt = $scope.plotdata_org[res.data.length-1];
                $scope.lag = 0;
                //console.log($scope.plotdata_org[0]['yearMonth']); // debug

                // Also obtain the PCC value for the first brand select
                $http.get('msReader.jsp?pcc='+brs[0]+'&dtrng='+ $scope.br_sdt['yearMonth']+','+$scope.br_edt['yearMonth']).then(function(res){
                    $scope.pccdata = res.data;
                    //console.log($scope.data); // debug
                });
            });
        } else {
            $scope.sql_brs = 'msReader.jsp';
        }

        //refresh
        $http.get($scope.sql_brs).success(function(data, status){
            if (data && status === 200) {
                $scope.tbrecs = data;
            } else
                $scope.tbrecs = [];
            //console.log($scope.tbrecs); // debug
        });
    };

    $scope.filterdate = function (brs, sdt, edt, lag) {
        if (brs && edt > sdt)  {
            //console.log('sdate=',sdt,'edate=',edt,'lag=',lag);

            // Plot the first brand select
            $http.get('msReader.jsp?brgraph='+brs[0]+'&dtrng='+sdt+','+edt+'&lag='+lag).then(function(res){
                $scope.plotdata = res.data;
                //console.log($scope.data); // debug
            });

            // Also obtain the PCC value for the first brand select
            $http.get('msReader.jsp?pcc='+brs[0]+'&dtrng='+sdt+','+edt+'&lag='+lag).then(function(res){
                $scope.pccdata = res.data;
                //console.log($scope.data); // debug
            });
        }
    }


});








