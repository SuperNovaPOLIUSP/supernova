/**
  * class Questionnaire
  * Represent a questionnaire from the database.
  */
    /**
     * The database id of this questionnaire, if this is a new questionnaire the id is
     * null.
     */
    //idQuestionnaire 
    /**
     * This questionnaire assessment number in this opticalSheet, it goes from 1 to
     * ....
     */
    //assessmentNumber 
    /**
     * The set of instructions to be used for this questionnaire in the printed
     * OpticalSheet.
     */
    //instructions 
    /**
     * A html element div that belongs to the body of the html code and is a general
     * area to be used by the objects.
     */
    //optionsDiv 
    /**
     * This objects questionsList.
     */
    //questionsList 
    /**
     * A html element span that showes the assessment Number of this questionnaire to
     * the user.
     */
    //span 
    /**
     * A list of this object questionBoxes, the list have 10 objects.
     */
    //questionBoxes 
    /**
     * A boolean representing that this questionnaire is ready to be printed.
     */
    //okToPrint 
    /**
     * A boolean representing that this questionnaire is ready to be stored.
     */
    //okToSave 
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 


/**
* Initialization method.
* @param optionsDiv
* 
* @param idQuestionnaire
* If this is a new questionnaire it may be null.
* @param assessmentNumber
* Aways bigger than 0.
*/
function Questionnaire(optionsDiv, idQuestionnaire, assessmentNumber){
    this.idQuestionnaire = idQuestionnaire
    this.assessmentNumber = assessmentNumber
    this.div = $(document.createElement('div'))
    this.div.attr('id',"questionnaire")
    this.div.attr('name',"questionnaire")
    this.div.attr('style','position:absolute; top:0px; left:10px; display:block')
    this.instructions = new Instructions()
    this.optionsDiv = optionsDiv
    this.questionsList = new QuestionsList()   
    
    this.span = $(document.createElement('span')) 
    this.span.text('AssessmentNumber:' + this.assessmentNumber)
    this.span.attr('style', 'position:absolute; top:630; left:100')

    this.questionBoxes = new Array()
    for (var i = 0; i < 10; i++){
        this.questionBoxes[i] = new QuestionBox(i, null, this)
    }
    this.okToPrint = true
    this.okToSave = true

    this.showQuestionnaire()
}

/**
 * Check and set the okToSave and okToPrint bool.
 */
Questionnaire.prototype.checkState = function(){
    this.okToPrint = true
    this.okToSave = true
    for (var i = 0; i < 10; i++){
        if (!this.questionBoxes[i].ready){
            this.okToSave = false
        }
        if (this.questionBoxes[i].changed || !this.questionBoxes[i].ready){
            this.okToPrint = false
        }
    }
}

/**
 * Is called by the given questionBox, this shows in the optionsDiv the answerTypes
 * to be selected by the questionBox for its store method.
 * @param questionBox
    *      QuestionBox that wants its question to be stored.
 */
Questionnaire.prototype.createQuestion = function (questionBox){
    this.optionsDiv.children().detach()
    this.questionsList.createQuestion(questionBox, this.instructions.answerTypes)
    this.optionsDiv.append(this.questionsList.div)
}

/**
 * Renew this questionnare div element, to keep up with its children changes.
 */
Questionnaire.prototype.showQuestionnaire = function(){
    //this.div.empty()
    this.div.children().detach()
    questionsDiv = $(document.createElement('div'))
    questionsDiv.attr('id', 'questionsDiv')
    questionsDiv.attr('name', 'questionsDiv')
    questionsDiv.attr('style','position:absolute; top:115px; left:0px; display:block')
    for (var i = 0; i < 10; i++){
        questionsDiv.append(this.questionBoxes[i].div)
    }
    this.div.append(questionsDiv)
    this.instructions.updateInstructions(this.questionBoxes)
    this.div.append(this.instructions.div)
    this.div.append(this.span)
}

/**
 * Showes the list of questions from the questionsList search in the optionsDiv.
 * @param searchedQuestionWording
    *      Part of the questionWording of the wanted question.
 * @param questionBox
    *      The questionBox from where this function was called.
 */
Questionnaire.prototype.showQuestionList = function(searchQuestionWording, questionBox){
    this.questionsList.search(searchQuestionWording)
    this.questionsList.showList(questionBox)
    this.optionsDiv.children().detach()
    this.optionsDiv.append(this.questionsList.div)

    createQuestionButton = new $(document.createElement('button'))
    createQuestionButton.text('createQuestion')
    createQuestionButton.mousedown(this.createQuestion.bind(this, questionBox))
    createQuestionButton.attr('style', 'position:absolute; top:325px; left:0px;')

    this.optionsDiv.append(createQuestionButton)
    this.optionsDiv.show()
}

/**
 * Creates a new QuestionBox object and place it on top of the old one with the
 * same number. Ps.  index = (questionBox.number + 1)
 * @param question
    *      Question object to be loaded.
 * @param index
    *      Number from 1-10 that defines the position in which this question will be
    *      placed.
 */
Questionnaire.prototype.loadQuestion = function(question, index){
    //index goes from 1 - 10
    questionBox = new QuestionBox(index - 1, question, this)
    this.questionBoxes[index - 1] = questionBox
    this.showQuestionnaire()
}

/**
 * returns the data of this questionnaire, it is a dict with the keys:
 * questions: [questionbox1.getdata(), ...]
 * idquestionnaire
 * assessmentnumber
 * instructions: instructions.getdata()
 */
Questionnaire.prototype.getData = function(){
    questionsData = new Array()
    for (var i in this.questionBoxes){
        questionsData.push(this.questionBoxes[i].getData())
    }
    instructionsData = this.instructions.getData()
    data = {
        questions: questionsData,
        idQuestionnaire: this.idQuestionnaire,
        assessmentNumber: this.assessmentNumber,
        instructions: instructionsData 
    }
    return data
}
