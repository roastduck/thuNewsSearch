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
    .controller('IndexController', ['$scope', '$timeout', '$sce', 'load', function($scope, $timeout, $sce, load) {
        $scope.searchInput = '';
        $scope.page = 1;
        $scope.result = [];
        $scope.notify = function() { // notify change of $scope.searchInput
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
    }])

