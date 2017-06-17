var ssHelperApp = angular.module('ssHelperApp', []);
ssHelperApp.controller('csvCtrl', function ($scope, $sce, $http) {
    // First time init of Star Schema csv files
    $http.get('ssReader/')
        .success(function (data, status) {
            if (data && status === 200) {
                $scope.ssdata = data;
                //console.log($scope.ssdata); // debug
            }
    });

    $scope.filterfield = function (kwd) {
        //console.log(kwd); //debug
        if (kwd.length>0) {
            var kwds = '(';
            for (var i=0; i< kwd.length; i++) {
                kwds += kwd[i]+'|';
            }
            kwds = kwds.slice(0,-1) + ')';
            $scope.qry_kwd = 'ssReader/?kwd='+ kwds+ '$';
            //console.log($scope.qry_kwd); //debug
        } else {
            $scope.qry_kwd = 'ssReader/';
        }

        // Refresh
        $http.get($scope.qry_kwd).success(function(data, status){
            if (data && status === 200) {
                $scope.ssdata = data;
            }
            console.log($scope.ssdata); // debug
        });
    };
});


