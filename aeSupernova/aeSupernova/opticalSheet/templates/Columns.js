/**
  * class Columns
  * The set of columns in the opticalSheet site.
  */

    /**
     * An array of 20 Column objects, initialy all are empty.
     */
    //columns
    /**
     * A html element button that execute the createSwitchColumns method.
     */
    //switchButton
    /**
     * A html element div that belongs to the body of the html code and is a general
     * area to be used by the objects.
     */
    //optionsDiv
    /**
     * A CourseList object to be used in this object.
     */
    //coursesList
    /**
     * Database id of the timePeriod used in this columns.
     */
    //idTimePeriod
    /**
     * A boolean representing that this Columns is ready to be printed.
     */
    //okToPrint
    /**
     * A boolean representing that this Columns is ready to be stored.
     */
    //okToSave
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div

/**
 * 
 * @param optionsDiv
    *      
 * @param idTimePeriod
    *      
 * @param idCycle
    *      Database id of the opticalSheet's cycle, it is going to be used in the
    *      CoursesList.
 * @param term
    *      The term of the relation between the opticalSheet and the cycle, is going to be
    *      used in the CoursesList.
 */
function Columns(optionsDiv, idTimePeriod, idCycle, term){
    this.columns = new Array()
    this.div = $(document.createElement('div'))
    this.div.attr('id', 'Columns')
    this.div.attr('name', 'Columns')
    this.div.attr('style','position:absolute; top:0px; left:415px; display:block;')


    this.switchButton = $(document.createElement('button'))
    this.switchButton.attr('style','position:absolute; top:100px; left:400px; display:block;')
    this.switchButton.text('switch')
    this.switchButton.mousedown(this.createSwitchColumns.bind(this))

    for (var i = 0; i < 20; i++){
        this.columns[i] = new Column(i, null, this)
    }

    this.optionsDiv = optionsDiv 
    this.optionsDiv.hide()

    this.coursesList = new CoursesList(idTimePeriod, idCycle, term)
    this.idTimePeriod = idTimePeriod
    this.okToSave
    this.okToPrint
    this.showColumns()
}

/**
 * Check and set the okToSave and okToPrint bool.
 */
Columns.prototype.checkState = function(){
    this.okToPrint = true
    this.okToSave = true
    for (var i = 0; i < 20; i++){
        if (!this.columns[i].ready){
            this.okToSave = false
        }
        if (this.columns[i].changed || !this.columns[i].ready){
            this.okToPrint = false
        }
    }
}

/**
 * Renew this columns div element, to keep up with its children changes.
 */
Columns.prototype.showColumns = function(){
    this.div.children().detach()

    columnsDiv = $(document.createElement('div'))
    columnsDiv.attr('id', 'columns')
    columnsDiv.attr('name', 'columns')
    for (var i = 0; i < 20; i++){
        columnsDiv.append(this.columns[i].div)
    }
    this.div.append(columnsDiv)
    this.div.append(this.switchButton)
    this.checkState()
}

/**
 * Create the html elements in the optionsDiv to allow the user to change two
 * Column places.
 */
Columns.prototype.createSwitchColumns = function(){
    column1 = $(document.createElement('select'))
    this.optionsDiv.children().detach()
    for (var i = 0; i <= 20; i++){
        option = $(document.createElement('option'))
        option.attr('value',i)
        if (i>0){
            option.text(String(i))
        }
        column1.append(option)
    }
    column2 = column1.clone()
    this.optionsDiv.append(column1)
    this.optionsDiv.append(column2)
    this.optionsDiv.show()
    column1.change(this.switchColumns.bind(this, column1, column2))
    column2.change(this.switchColumns.bind(this, column1, column2))
}

/**
 * Changes the two columns in the selected position, if the ints given are greater
 * than 0.
 * @param column1
    *      Represents the column to be switched, it goes from 0(invalid) to 20.
 * @param column2
    *      Represents the column to be switched, it goes from 0(invalid) to 20.
 */
Columns.prototype.switchColumns = function(column1,column2){
    column1 = column1.val() - 1
    column2 = column2.val() - 1
    if (column1 >= 0 && column2 >= 0){
        if (!this.columns[column1].ready || !this.columns[column2].ready){
            alert('não pode trocar colunas que não estão prontas')
        } else {
            if (this.columns[column1].course != null){
                var tempCourse = this.columns[column1].course.clone()
            } else {
                var tempCourse = null
            }
            if (this.columns[column2].course != null){
                this.columns[column1].setCourse(this.columns[column2].course.clone(), this.idTimePeriod)
            } else {
                this.columns[column1].setCourse(null, this.idTimePeriod)
            }
            this.columns[column2].setCourse(tempCourse, this.idTimePeriod)
            this.optionsDiv.html('')
            this.optionsDiv.hide()
        }
    }
}

/**
 * Call and show the coursesList search for the given parameters in the optionsDiv.
 * @param searchedCourseCode
    *      CourseCode to be searched in the CoursesList, if it is empty it won't be used.
 * @param searchedAbbreviation
    *      Abbreviation to be searched in the CoursesList, if it is empty it won't be used.
 * @param column
    *      Column from where the user is requesting the search.
 */
Columns.prototype.showCoursesList = function(searchCourseCode, searchAbbreviation,column){
    this.coursesList.search(searchCourseCode, searchAbbreviation)
    this.coursesList.showCoursesList(column)
    this.optionsDiv.children().detach()
    this.optionsDiv.append(this.coursesList.div)
    this.optionsDiv.show()
}

/**
 * Load a course in a column. Using this method the Column's change is not set to
 * true.
 * @param course
    *      Course to be loaded in the column
 * @param index
    *      Number from 1 - 20  representing the column in with the given course will be
    *      placed.
 */
Columns.prototype.loadColumn = function(course,index){
    //index goes from 1 - 20
    column = new Column(index - 1, course, this)
    this.columns[index - 1] = column
    this.showColumns()
}

/**
 * Return a list where each element is the getData response of this objects
 * columns.
 */
Columns.prototype.getData = function(){
    columnsData = new Array() 
    for (var i in this.columns){
        columnsData[i] = this.columns[i].getData()
    }
    return columnsData
}

