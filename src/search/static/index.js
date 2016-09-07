angular.module('appIndex', [])
    .service('load', ['$http', function($http) {
        this.update = function(words, page, filtertype, callback) { // callback : fn(retrieved list)
            $http({
                method: 'GET',
                url: '/api/search',
                params: {
                    q: words,
                    page,
                    filtertype
                }
            }).then(function(response) {
                callback(response.data)
            });
        };
    }])
    .controller('IndexController', ['$scope', '$timeout', '$sce', '$location', 'load', function($scope, $timeout, $sce, $location, load) {
        var update = function() { // update data
            var searchInput = $location.search()['q']; // not in $scope for situation that user is typing
            $scope.page = $location.search()['page'];
            $scope.filtertype = $location.search()['filtertype'];
            if (searchInput === undefined) searchInput = '';
            if ($scope.page === undefined) $scope.page = 1;
            if ($scope.filtertype == undefined) $scope.filtertype = "0";

            if (searchInput == '')
            {
                $scope.result = [];
                $timeout(function() {
                    $("#maininput").focus();
                });
                return;
            }
            load.update(searchInput.split(' '), $scope.page, $scope.filtertype, function(result) {
                $scope.result = result.map(function(row) {
                    row['title'] = $sce.trustAsHtml(row['title']);
                    row['content'] = $sce.trustAsHtml(row['content']);
                    return row;
                });
                $timeout(function() {
                    if ($scope.result.length)
                        $("#navinput").focus();
                    else
                        $("#maininput").focus();
                });
            });
            window.scrollTo(0, 0);
        };
        $scope.$on('$locationChangeSuccess', update);
        update();

        var notify = function() { // notify change of $scope.searchInput
            $location.search('q', $scope.searchInput);
            $location.search('page', $scope.page);
            $location.search('filtertype', $scope.filtertype);
        };

        $scope.searchInput = $location.search()['q'];
        if ($scope.searchInput === undefined) $scope.searchInput = '';
        $scope.result = [];
        $scope.nextPage = function() {
            $scope.page ++;
            notify();
        };
        $scope.prevPage = function() {
            $scope.page --;
            notify();
        };
        $scope.updsearch = function() {
            $scope.page = 1;
            $scope.filtertype = "0";
            notify();
        };
        $scope.updfilter = function() {
            $scope.page = 1;
            notify();
        };
    }]);

