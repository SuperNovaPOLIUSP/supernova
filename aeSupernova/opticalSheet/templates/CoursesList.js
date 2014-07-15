/**
  * class CoursesList
  * A object to show the options of courses to put in a column.
  */
    /**
     * A list of Course objects that will be shown in the list.
     */
    //chosenCourses 
    /**
     * The assossiated id with the timePeriod in the database.
     */
    //idTimePeriod 
    /**
     * The assossiated id with the opticalSheet's cycle in the database.
     */
    //idCycle 
    /**
     * The term of the relation between the opticalSheet and the cycle.
     */
    //term 
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 
    /**
     * A list with all the courses in the database, this is created in getCurses()
     * method.
     */
    //courses 


function CoursesList(idTimePeriod, idCycle, term){
    this.chosenCourses = new Array()
    this.courses = new Array()
    this.idTimePeriod = idTimePeriod
    this.idCycle = idCycle
    this.term = term
    this.div = $(document.createElement('div'))
    this.div.attr('id', 'CoursesList')
    this.div.attr('name', 'CoursesList')
    this.getCourses()
}

/**
 * This method searches in its courses list by a course with parameters like the
 * given ones, and place them in the chosenCourses list.
 * @param courseCode
    *      CourseCode to be searched in the CoursesList, if it is empty it won't be used.
 * @param abbreviation
    *      Abbreviation to be searched in the CoursesList, if it is empty it won't be used.
 */
CoursesList.prototype.search = function(courseCode, abbreviation){
    this.chosenCourses = new Array()
    for (var i in this.courses){
        if (this.courses[i].courseCode.indexOf(courseCode) != -1 && this.courses[i].abbreviation.indexOf(abbreviation) != -1){
           this.chosenCourses.push(this.courses[i]) 
        } 
    }
}

/**
 * Send a GET to /opticalSheet/getCurses with the parameters idCycle, term and
 * idTimePeriod, and recives all the courses in the database, in for of dicts, the
 * ones that belong to de cycle, term, timePeriod passed will be preferencial. With
 * the dicts create Course object and place them in the courses list.
 */
CoursesList.prototype.getCourses = function(){
    get = new XMLHttpRequest()
    get.open( "GET", 'getCourses/?' + $.param({idCycle : this.idCycle, term : this.term, idTimePeriod : this.idTimePeriod}), false)
    get.send(null)
    var coursesData = JSON.parse(get.responseText)
    this.courses = new Array()
    for (var i in coursesData){
        course = new Course(coursesData[i]['courseCode'], coursesData[i]['courseName'], coursesData[i]['courseAbbreviation'], coursesData[i]['idCourse'], [], coursesData[i]['oneOfTheFirst'])
        this.courses[i] = course
    }

}

/**
 * This method sends a GET to /opticalSheet/expandCourse with the parameters
 * idTimePeriod and idCourse. The result is a list of courses in the form of dicts,
 * where each one is a possible expansion of the given one. For instance PQI2110 ->
 * PQI2110(T), PQI2110(P), PQI2110[ProfessorX]...
 * @param course
    *      The Course to be expanded.
 * @param idTimPeriod
    *      The idTimePeriod of the course to be expanded.
 * @param column
    *      The Column from where this expansion was requested.
 */
CoursesList.prototype.expandCourse = function(course, idTimePeriod, column){
    get = new XMLHttpRequest()
    get.open( "GET", 'expandCourse/?' + $.param({idTimePeriod : this.idTimePeriod, idCourse : course.idCourse}), false)
    get.send(null)
    var coursesData = JSON.parse(get.responseText)
    this.chosenCourses = new Array()
    for (var i in coursesData){
        course = new Course(coursesData[i]['courseCode'], coursesData[i]['courseName'], coursesData[i]['courseAbbreviation'], coursesData[i]['idCourse'], [], coursesData[i]['oneOfTheFirst'])
        this.chosenCourses[i] = course
    }
    this.showCoursesList(column) 
}

/**
 * Puts in the div all the chosenCourses list elements in the form of span and
 * buttons, for the user select which one will be placed in the column or expanded.
 * @param column
    *      The Column that requested this method.
 */
CoursesList.prototype.showCoursesList = function(column){
    this.div.empty()
    span = $(document.createElement('span'))
    span.text('seleção de disicplinas para a coluna ' + String(column.number + 1) + ':')
    this.div.append(span)
    select = $(document.createElement('div'))
    select.attr('size',12)
    select.attr('style','width: 1000px;height: 300px; overflow-y: scroll;')
    for (var i in this.chosenCourses){
            var courseDiv = new $(document.createElement('div'))
            var option = new $(document.createElement('span'))
            option.text(this.chosenCourses[i].abbreviation + '-' + this.chosenCourses[i].courseCode)
            if (this.chosenCourses[i].preferential){
                option.attr('style','color:blue')
            }
            var addButton = new $(document.createElement('button'))
            addButton.html('add')
            addButton.mousedown(column.setCourse.bind(column, this.chosenCourses[i], this.idTimePeriod))
            addButton.attr('style', 'float: right; height = 25px')
            var expandButton = new $(document.createElement('button'))
            expandButton.attr('style', 'float: right; height = 25px')
            expandButton.html('expand')
            expandButton.mousedown(this.expandCourse.bind(this, this.chosenCourses[i], this.idTimePeriod, column))

            courseDiv.append(option)
            courseDiv.append(expandButton)
            courseDiv.append(addButton)
            courseDiv.attr('style', 'height: 30px; border:1px solid black;')
            select.append(courseDiv)
    }
    this.div.append(select)
}
