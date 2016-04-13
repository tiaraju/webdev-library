(function () {
	var library= angular.module('library',['ngAnimate', 'ui.bootstrap']);
	library.controller('libraryController',function($scope, $uibModal,$http){
		var self = this;

		//self.books=collection;
		
		$scope.comment;
		$scope.book = {}
		$scope.bookID;
		
		$scope.init = function () {
			$http.get("/books")
			.then(function(response) {
				self.books = response.data;
				console.log(self.books);
			},
			function(error){
				alert("Unnable to retrieve the collection");
			}); 
		}

		$scope.init();

	    $scope.setBookId=function(id) {
	    	 $scope.bookID = id;
	    };

	    $scope.showModal = function(){
		    $scope.modalInstance = $uibModal.open({
		      animation: $scope.animationsEnabled,
		      templateUrl: '../static/modal.html',
		      controller: 'libraryController',
			  preserveScope:true,
		      clickOutsideToClose: true,
		      scope:$scope
		    });
		    
		 };

		$scope.toggleAnimation = function () {
    		$scope.animationsEnabled = !$scope.animationsEnabled;
  		};

  		$scope.addBook = function (newbook) {
  			$scope.book = newbook;
			$http({
			    url: "/books",
			    method: "POST",
			    data: $scope.book,
			    headers: {
			        'Content-Type': 'application/json; charset=UTF-8',
			        'Accept': 'application/json'
			    }
			}).then(function(response) {
				alert("Book Registered");
				//$scope.cancel();
    			$scope.modalInstance.close();
			},
			function(error){
				alert("Nao foi possivel salvar o livro.")
    			$scope.modalInstance.close();
			});
  		};

  		$scope.showCommentDialog = function(){
  			 $scope.modalInstance = $uibModal.open({
		      animation: $scope.animationsEnabled,
		      templateUrl: '../static/commentModal.html',
		      controller: 'libraryController',
			  preserveScope:true,
		      clickOutsideToClose: true,
		      scope:$scope
		    });

  		};

  		$scope.saveComment = function(comentario){
  			console.log(comentario);
  			self.books[$scope.bookID].comments.push(comentario);
			$scope.modalInstance.close();
  		};

  		$scope.cancel = function () {
    		$scope.modalInstance.dismiss('cancel');
  		};

	});
})();