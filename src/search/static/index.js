angular.module('appIndex', [])
    .service('load', ['$http', function($http) {
        this.update = function(words, page, callback) { // callback : fn(retrieved list)
            $http({
                method: 'GET',
                url: '/api/search',
                params: {
                    q: words,
                    page: page
                }
            }).then(function(response) {
                callback(response.data)
            });
        };
    }])
    .controller('IndexController', ['$scope', '$timeout', '$sce', '$location', 'load', function($scope, $timeout, $sce, $location, load) {
        $scope.searchInput = $location.search()['q'];
        $scope.page = $location.search()['page'];

        if ($scope.searchInput === undefined) $scope.searchInput = '';
        if ($scope.page === undefined) $scope.page = 1;

        $scope.result = [];

        $scope.notify = function() { // notify change of $scope.searchInput
            $location.search('q', $scope.searchInput);
            $location.search('page', $scope.page);
            if ($scope.searchInput == '')
            {
                $scope.result = [];
                $timeout(function() {
                    $("#maininput").focus();
                });
                return;
            }
            load.update($scope.searchInput.split(' '), $scope.page, function(result) {
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
        };

        $scope.notify();
    }])

