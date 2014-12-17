/**
  * class Course
  * Represent a course from the database.
  */
    /**
     * A 7 characters code that represent the course, it can be followed by a
     * complement that represent this specific set of offers
     */
    //courseCode
    /**
     * The name of this course.
     */
    //name
    /**
     * The abbreviation is the string that will be shown in the opticalSheet.
     */
    //abbreviation
    /**
     * The database id assossiated with this object.
     */
    //idCourse
    /**
     * A list of idOffers that form this course, this may be null until this course is
     * placed in a column.
     */
    //idOffers
    /**
     * A boolean that represents if this course is to be seen as special by the
     * CourseList.
     */



/**
 * Initialization method
 * @param courseCode
    *      A 7 characters code that represent the course, it can be followed by a
    *      complement that represent this specific set of offers.
 * @param name
    *      The name of this course.
 * @param abbreviation
    *      The abbreviation is the string that will be shown in the opticalSheet, it may
    *      contain complement that represent this specific set of offers.
 * @param idCourse
    *      The database id assossiated with this object.
 * @param idOffers
    *      A list of idOffers that form this course, this may be null until this course is
    *      placed in a column.
 * @param preferential
    *      A boolean that represents if this course is to be seen as special by the
    *      CourseList.
 */
function Course(courseCode, name, abbreviation, idCourse, idOffers, preferential){
    this.courseCode = courseCode 
    this.name = name
    this.abbreviation = abbreviation
    this.idCourse = idCourse
    this.idOffers = idOffers
    this.preferential = preferential //boolean showing if this course is to be placed in the top of the coursesList 
}

/**
 * Using the idTimePeriod and the courseCode of this object, a get is send to
 * 'findOffers/' and the return fill this object idOffers parameter.
 * @param idTimePeriod
    *      Id of an object timePeriod in the database.
 */
Course.prototype.findOffers = function(idTimePeriod){
    get = new XMLHttpRequest()
    get.open( "GET", 'findOffers/?' + $.param({idTimePeriod : idTimePeriod, courseCode : this.courseCode}), false)
    get.send(null)
    this.idOffers  = JSON.parse(get.responseText)
}

/**
 * Returns a clone of this object.
 */
Course.prototype.clone = function(){
    var copy = new Course(this.courseCode, this.name, this.abbreviation, this.idCourse, this.idOffers)
    return copy
}
