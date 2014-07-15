/**
  * class Positions
  * This is a group of options for the print functions.
  */
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 
    /**
     * A div to set the horizontal position of the set of questions on the opticalSheet
     * to be printed.
     */
    //questionnaireX 
    /**
     * A div to set the vertical position of the set of questions on the opticalSheet
     * to be printed.
     */
    //questionnaireY 
    /**
     * A div to set the vertical distance between the questions on the opticalSheet to
     * be printed.
     */
    //questionnaireDY 
    /**
     * A div to set the horizontal position of the set of courses on the opticalSheet
     * to be printed.
     */
    //columnsX 
    /**
     * A div to set the vertical position of the set of courses on the opticalSheet to
     * be printed.
     */
    //columnsY 
    /**
     * A div to set the horizontal distance between the courses on the opticalSheet to
     * be printed.
     */
    //columnsDX 
    /**
     * A div to set the horizontal position of the set of instructions on the
     * opticalSheet to be printed.
     */
    //tableX 
    /**
     * A div to set the vertical position of the set of instructions on the
     * opticalSheet to be printed.
     */
    //tableY 
    /**
     * A div to set the number of line for each course in the qualitative questionnaire
     * to be printed.
     * 
     */
    //numberOfLines 
    /**
     * A div to set if the courses on the qualitative questionnaire will be shown by
     * name or not.
     */
    //qualitativeQuestionnaireType 
    /**
     * A div to select if the download of the printed opticalSheet or qualitative
     * questionnaire will be of the pdf or the tex (LaTeX) file
     */
    //downloadType 



function Positions(){
    this.div = $(document.createElement('div'))
    this.div.attr('id', 'positions')
    this.div.attr('style','position:absolute; left:1600px;top:300px')

    this.questionnaireX = this.createPosition('questionnaireX', 0.5)
    this.questionnaireX.attr('style', 'position:absolute;top:0px;')
    this.questionnaireY = this.createPosition('questionnaireY', 7.6)
    this.questionnaireY.attr('style', 'position:absolute;top:25px;')
    this.questionnaireDY = this.createPosition('questionnaireDY', 1.4)
    this.questionnaireDY.attr('style', 'position:absolute;top:50px;')
    
    this.columnsX = this.createPosition('columnsX', 9.0)
    this.columnsX.attr('style', 'position:absolute;top:75px;')
    this.columnsY = this.createPosition('columnsY', 2.2)
    this.columnsY.attr('style', 'position:absolute;top:100px;')
    this.columnsDX = this.createPosition('columnsDX', 2.8)
    this.columnsDX.attr('style', 'position:absolute;top:125px;')
    
    this.tableX = this.createPosition('tableX', 0.5)
    this.tableX.attr('style', 'position:absolute;top:150px;')
    this.tableY = this.createPosition('tableY', 3.5)
    this.tableY.attr('style', 'position:absolute;top:175px;')

    this.numberOfLines = $(document.createElement('div'))
    this.numberOfLines.attr('style','position:absolute;top:200px;')
    span = $(document.createElement('span'))
    span.attr('style', 'position:absolute; top:0px')
    span.text('Number of lines')
    numberOfLinesSelect = $(document.createElement('select'))
    numberOfLinesSelect.attr('style', 'position:absolute; top:0px; left:120px')
    for (var i = 4; i >0; i--){
        var option = $(document.createElement('option'))
        option.text(i)
        option.val(i)
        numberOfLinesSelect.append(option)
    }
    this.numberOfLines.append(span)
    this.numberOfLines.append(numberOfLinesSelect)

    this.qualitativeQuestionnaireType = $(document.createElement('div'))
    this.qualitativeQuestionnaireType.attr('style','position:absolute;top:240px;')
    span = $(document.createElement('span'))
    span.text('Qualitative questionnaire type')
    qqTypeSelect = $(document.createElement('select'))
    qqTypeSelect.attr('style', 'position:absolute; top:0px; left:120px')
    var option = $(document.createElement('option'))
    option.text('normal')
    option.val(0)
    qqTypeSelect.append(option)
    var option = $(document.createElement('option'))
    option.text("No course's name")
    option.val(1)
    qqTypeSelect.append(option)
    this.qualitativeQuestionnaireType.append(span)
    this.qualitativeQuestionnaireType.append(qqTypeSelect)

    this.downloadType = $(document.createElement('div'))
    this.downloadType.attr('style','position:absolute;top:300px;')
    span = $(document.createElement('span'))
    span.text('Download type')
    downloadTypeSelect = $(document.createElement('select'))
    downloadTypeSelect.attr('style', 'position:absolute; top:0px; left:120px')
    var option = $(document.createElement('option'))
    option.text('pdf')
    option.val('pdf')
    downloadTypeSelect.append(option)
    var option = $(document.createElement('option'))
    option.text("tex")
    option.val('tex')
    downloadTypeSelect.append(option)
    this.downloadType.append(span)
    this.downloadType.append(downloadTypeSelect)

    this.div.append(this.questionnaireX)
    this.div.append(this.questionnaireY)
    this.div.append(this.questionnaireDY)
    this.div.append(this.columnsX)
    this.div.append(this.columnsY)
    this.div.append(this.columnsDX)
    this.div.append(this.tableX)
    this.div.append(this.tableY)
    this.div.append(this.numberOfLines)
    this.div.append(this.qualitativeQuestionnaireType)
    this.div.append(this.downloadType)

}

/**
 * Return all the data from this object as a dict where each key is one of this
 * objects div.
 */
Positions.prototype.getData = function(){
    positions = {
        questionnaireX: this.questionnaireX.children('textarea').eq(0).val(),
        questionnaireY: this.questionnaireY.children('textarea').eq(0).val(),
        questionnaireDY: this.questionnaireDY.children('textarea').eq(0).val(),

        columnsX: this.columnsX.children('textarea').eq(0).val(),
        columnsY: this.columnsY.children('textarea').eq(0).val(),
        columnsDX: this.columnsDX.children('textarea').eq(0).val(),

        tableX: this.tableX.children('textarea').eq(0).val(),
        tableY: this.tableY.children('textarea').eq(0).val(),
        
        numberOfLines: this.numberOfLines.children('select').eq(0).val(),
        qualitativeQuestionnaireType: this.qualitativeQuestionnaireType.children('select').eq(0).val(),
        downloadType: this.downloadType.children('select').eq(0).val()
    }
    return positions
}

/**
 * Internal method to help create this objects many divs.
 * @param name
    *      Name of the div to be created.
 * @param value
    *      Initial value of this div's textarea.
 */
Positions.prototype.createPosition = function(name, value){
    positionDiv = $(document.createElement('div'))
    positionDiv.attr('id',name)
    positionDiv.attr('name',name)
    textArea = $(document.createElement('textarea'))
    textArea.attr('style','position:absolute;left:120px ;width: 50px;height: 25px;font-size: 12;resize: none;')
    textArea.attr('contentEditable',true);
    textArea.val(value)
    span = $(document.createElement('span'))
    span.text(name)
    span.attr('style','position:absolute; left:0px; font-size: 12')
    positionDiv.append(span)
    positionDiv.append(textArea)
    return positionDiv
   
}
