/**
  * class Column
  * A single opticalSheet's column.
  */
    /**
     * A number from 0 - 19 representing the position of this Column in the Columns.
     */
    //number
    /**
     * The Course belonging to this Column, it may be null.
     */
    //course
    /**
     * The Columns object that this Column belongs to.
     */
    //father
    /**
     * Boolean representing that this Column is ready to be stored.
     */
    //ready
    /**
     * Boolean representing that this Column has been changed.
     */
    //changed
    /**
     * A html element textarea that allows the user to set this column font.
     */
    //fontTextbox
    /**
     * A html element textarea that allows the user to set this column course.
     */
    //codeTextbox
    /**
     * A html element textarea that allows the user to set this column course's
     * abbreviation.
     */
    //abbreviationTextbox
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div

/**
 * Initialization method.
 * @param number
    *      
 * @param course
    *      
 * @param father
    *      
 */
function Column(number, course, father){
    /*
    course can be null
    */

    this.father = father
    this.number = number
    
    this.ready = true
    this.changed = false 

    this.fontTextbox = $(document.createElement('textarea'))
    this.fontTextbox.attr('style','position:absolute; top:70px;left:25px; border:0.5px solid #000000;width:25px;height:25px;resize: none;')
    this.fontTextbox.attr('id', 'courseFont' + this.number)
    this.fontTextbox.attr('name', 'courseFont' + this.number)
    this.fontTextbox.val('9')
    this.fontTextbox.attr('contentEditable',true)

    this.codeTextbox = $(document.createElement('textarea'))
    this.codeTextbox.attr('style','position:absolute; border:0.5px solid #000000;width: 100px;height: 20px;font-size: 12;resize: none;')
    this.codeTextbox.attr('id','courseCode' + this.number)
    this.codeTextbox.attr('name','courseCode' + this.number)
    this.codeTextbox.attr('contentEditable',true);
    this.codeTextbox.keyup(this.codeChanged.bind(this))    


    this.abbreviationTextbox = $(document.createElement('textarea'))
    this.abbreviationTextbox.attr('style','position:absolute; top:20px; border:0.5px solid #000000;width: 100px;height: 50px; font-size: 12;resize: none;')
    this.abbreviationTextbox.attr('id','courseAbbreviation' + this.number)
    this.abbreviationTextbox.attr('name','courseAbbreviation'+ this.number)
    this.abbreviationTextbox.attr('contentEditable',true)

    this.div = $(document.createElement('div'))
    this.div.attr('id','column' + this.number)
    this.div.attr('name','column' + this.number)
    this.div.attr('style','position:absolute; left:' + String(this.number*110)  + 'px; display:block')
    this.div.append(this.fontTextbox)
    this.div.append(this.codeTextbox)
    this.div.append(this.abbreviationTextbox)
    if (course == null){
        this.course = null
    } else{
        this.course = course
        this.abbreviationTextbox.val(course.abbreviation)
        this.codeTextbox.val(course.courseCode)
    }
}

/**
 * Is to be called if codeTextbox changes, it compares the codeTextbox content with
 * the course's courseCode. If it is diferent and not empy marks this Column as not
 * ready and show a list of Courses that match this courseCode, if it is empty, set
 *  this course as null.
 */
Column.prototype.codeChanged = function(){
    if (this.course != null){
        courseCode = this.course.courseCode
    } else {
        courseCode = ''
    }
    if (this.codeTextbox.val() != courseCode){
        if (this.codeTextbox.val() == ''){
            this.setCourse(null, null)
        } else {
            this.father.showCoursesList(this.codeTextbox.val(),'', this)
            this.ready = false
        }
    } else {
        this.ready = true
    }
    this.showState()
}


/**
 * Shows the Column as red if not ready and as green if changed.
 */
Column.prototype.showState = function(){
    if (!this.ready){
        color = '#FE2E2E'
    } else if (this.changed) {
        color = '#00FF00'
    } else {
        color = '#FFFFFF'
    }
    this.abbreviationTextbox.css("background-color",color)
    this.codeTextbox.css("background-color",color) 
}

/**
 * Returns a dictionary with this Column data, with the keys: courseCode,
 * abbreviation, font, idCourse, idOffers, courseIndex.
 */
Column.prototype.getData = function(){
    if (this.course != null){
        data = {
            courseCode: this.course.courseCode.replace(/;/g,'%3B'),
            abbreviation: this.abbreviationTextbox.val(),
            font: parseInt(this.fontTextbox.val()),
            idCourse: this.course.idCourse,
            idOffers: this.course.idOffers,
            courseIndex: this.number
        }
    } else {
        data = {
            courseCode: '',
            abbreviation: '',
            font: parseInt(this.fontTextbox.val()),
            idCourse: '',
            idOffers: '',
            courseIndex: this.number
        }
    }
    return data
}

/**
 * Sets the course in this object, along with the codeTextbox and the
 * abbreviationTextbox. If this course is not null it also calls the method
 * findOffers(idTimePeriod) of this course.
 * @param course
    *      Course object to be added in this Column, it may be null
 * @param idTimePeriod
    *      The assossiated id with the timePeriod in the database, it may be null only if
    *      the course is too.
 */
Column.prototype.setCourse = function(course, idTimePeriod){
    if (course != this.course){
        if (course != null){
            if (course.idOffers.length == 0) {
                course.findOffers(idTimePeriod)    
            }
            this.abbreviationTextbox.val(course.abbreviation)
            this.codeTextbox.val(course.courseCode)
        } else {
            this.abbreviationTextbox.val('')
            this.codeTextbox.val('')
        }
        this.course = course
        this.changed = true
        this.ready = true
        this.showState()
        this.father.showColumns()
    }
}

