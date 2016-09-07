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
        var update = function() { // update data
            var searchInput = $location.search()['q'];
            var page = $location.search()['page'];
            if (searchInput === undefined) searchInput = '';
            if (page === undefined) page = 1;

            if (searchInput == '')
            {
                $scope.result = [];
                $timeout(function() {
                    $("#maininput").focus();
                });
                return;
            }
            load.update(searchInput.split(' '), page, function(result) {
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
        };

        $scope.searchInput = $location.search()['q'];
        $scope.page = $location.search()['page'];
        if ($scope.searchInput === undefined) $scope.searchInput = '';
        if ($scope.page === undefined) $scope.page = 1;
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
            notify();
        };
    }]);

