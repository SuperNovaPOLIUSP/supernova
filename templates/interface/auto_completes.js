$(function() {
  	$("#ID_inputCourse").autocomplete({
    	source: "/interface/search_courses/",
    	minLength: 3,
  	});
});