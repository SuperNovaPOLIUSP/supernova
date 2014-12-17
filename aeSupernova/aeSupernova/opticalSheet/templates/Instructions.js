/**
  * class Instructions
  * This block of instructions on the top left of the site, it is also responsible 
  * for getting and holding all the answerTypes.
  */

    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 
    /**
     * A select that selects with instruction will show in the first column.
     */
    //select1 
    /**
     * A select that selects with instruction will show in the second column.
     */
    //select2 
    /**
     * A select that selects with instruction will show in the third column.
     */
    //select3 
    /**
     * A list with all the anwserType objects in the database.
     */
function Instructions(){
    this.div = $(document.createElement('div'))
    this.div.attr('id', 'instructions')
    this.div.attr('name', 'instructions')
    this.div.attr('style', 'position:absolute; top:0px; left:0px;')

    
    div1 = $(document.createElement('div'))
    div1.attr('style', 'position:absolute; top:0px; left:0px; display:block')
    this.select1 = $(document.createElement('select'))
    this.select1.attr('id', 'instructions1')
    this.select1.attr('name', 'instructions1')
    div1.append(this.select1)
    div1.append(this.createFonts())

    div2 = $(document.createElement('div'))
    div2.attr('style', 'position:absolute; top:30px; left:0px; display:block')
    this.select2 = $(document.createElement('select'))
    this.select2.attr('id', 'instructions2')
    this.select2.attr('name', 'instructions2')
    div2.append(this.select2)
    div2.append(this.createFonts())

    div3 = $(document.createElement('div'))
    div3.attr('style', 'position:absolute; top:60px; left:0px; display:block')
    this.select3 = $(document.createElement('select'))
    this.select3.attr('id', 'instructions3')
    this.select3.attr('name', 'instructions3')  
    div3.append(this.select3)
    div3.append(this.createFonts())



    this.div.append(div1)
    this.div.append(div2) 
    this.div.append(div3)

    this.answerTypes = this.getAnswerTypes()
}

/**
 * Internal function to create the font's textboxes for each select.
 */
Instructions.prototype.createFonts = function(){
    div = $(document.createElement('div'))
    for (var i = 0; i < 5; i++){
        textArea = $(document.createElement('textarea'))
        textArea.attr('style','position:absolute;top:0px;left:' + String(120 + i*30) + 'px ;width: 30px;height: 25px;font-size: 12;resize: none;')
        //textArea.attr('contentEditable',true);
        textArea.val(9)
        div.append(textArea)
    }
    return div
}


/**
 * Returns a list contening the information of each select in the form:
 * [{idAnswerType: idAnswerType1, fonts:[font11,font12...]}, {idAnswerType:
 * idAnswerType2, fonts:[font21,font22...]},{idAnswerType: idAnswerType3,
 * fonts:[font31,font32...]}]
 */
Instructions.prototype.getData = function(){
    instructionsData = new Array()
    for (var i=0; i < 3; i++){
        fonts = new Array()
        for (var j = 0; j < 5; j++){
            fonts.push(this.div.children('div').eq(i).children('div').eq(0).children('textArea').eq(j).val())
        }
        selectInfo = {
            idAnswerType: this.div.children('div').eq(i).children('select').eq(0).val(),
            fonts: fonts
        }
        instructionsData.push(selectInfo)
    }
    return instructionsData
}

/**
 * Send a GET to /opticalSheet/getAnswerTypes/ the response is a list with all the
 * database's answerTypes in the form of dicts, then they are transforment in
 * AnswerType objects and placed in the answerTypes list.
 */
Instructions.prototype.getAnswerTypes = function(){
    get = new XMLHttpRequest()
    get.open( "GET", 'getAnswerTypes/', false)
    get.send(null)
    var answerTypesData = JSON.parse(get.responseText)
    var answerTypesList = []
    for (var i in answerTypesData){
        answerType = new AnswerType(answerTypesData[i]['answerTypeName'], answerTypesData[i]['idAnswerType'], answerTypesData[i]['alternativeMeaning'])
        answerTypesList.push(answerType)
    }
    return answerTypesList
}

/**
 * Searches in the answerTypes list for an AnswerType object with the wanted
 * idAnswerType.
 * @param idAnswerType
    *      Assossiated database id of the wanted answerType.
 */
Questionnaire.prototype.findAnswerTypeById = function(idAnswerType){
    for (var i in this.answerTypes){
        if (this.answerTypes[i].idAnswerType == idAnswerType){
            return this.answerTypes[i]
        }
    }
    return null
}

/**
 * Checks which are the answerTypes of the questions in the questionnaire and place
 * this answerTypes in the select1,2,3.
 * @param questionBoxes
    *      List of all the questionnaire's questions.
 */
Instructions.prototype.updateInstructions = function(questionBoxes){
    option = $(document.createElement('option'))
    option.text('')
    option.val(0)
    this.select1.empty()
    this.select1.append(option)
    for (var i in this.answerTypes){
        for (var j in questionBoxes){
            if (questionBoxes[j].question != null && questionBoxes[j].question.idAnswerType == this.answerTypes[i].idAnswerType){
                option = $(document.createElement('option'))
                option.text(this.answerTypes[i].name)
                option.val(this.answerTypes[i].idAnswerType)
                this.select1.append(option)
                break
            }
        }
    }
    this.select2.empty()
    this.select3.empty()

    this.select1.children().clone().appendTo(this.select2)
    this.select1.children().clone().appendTo(this.select3)
}
