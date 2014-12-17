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
function Course(courseCode, name, offers){
    this.courseCode = courseCode 
    this.name = name
    this.offers = new Array()
    for (var i in offers){
        var offer = new Offer(offers[i]['idOffer'], offers[i]['professorName'], offers[i]['classNumber'])
        this.offers.push(offer)
    }
}

Course.prototype.getHTML = function(){
    var div = new $(document.createElement('div'))
    var sonsDiv = new $(document.createElement('div'))
    for (var i in this.offers){
        sonsDiv.append(this.offers[i].getHTML())
    }
    var span = new $(document.createElement('span'))
    span.text(this.courseCode + '-' + this.name)
    span.attr('style', 'font-size:14px')
    var input = new $(document.createElement('input'))
    input.attr('type','checkbox')
    input.change(function(){
        if (!input.attr('checked')){
            sonsDiv.find('input').each(function(){
                $(this).attr('checked', false);
            })
        } else {
            sonsDiv.find('input').each(function(){
                $(this).attr("checked", true);
            })
        }
    })
    input.val(0)
    div.append(input)
    div.append(span)
    div.append(sonsDiv)
    return div
}
