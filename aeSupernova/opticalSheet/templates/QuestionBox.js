/**
  * class QuestionBox
  * Represent one question area from the opticalSheet.
  */
    /**
     * Number of this question in the opticalSheet goes from 0 to 9.
     */
    //number 
    /**
     * The questionnaire from which this is questionBox belongs.
     */
    //father 
    /**
     * A html element textarea that allows the user to set this question font in the
     * printed opticalSheet.
     */
    //fontTextbox 
    /**
     * A html element textarea that allows the user to select the question of this
     * questionBox.
     */
    //questionTextbox 
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 
    /**
     * The Question that is represented by this object, it may be null.
     */
    //question 
    /**
     * Boolean representing that this questionBox is ready to be stored.
     */
    //ready 
    /**
     * Boolean representing that this questionBox has been changed.
     */
    //changed 


/**
 * Initialization method.
 * @param number
    *      
 * @param question
    *      The question to be assign to this object, it may be null.
 * @param father
    *      
 */
function QuestionBox(number, question, father){
    this.number = number
    if (number < 10){
        this.numberName = '0'+String(number)
    } else {
        this.numberName = String(number)
    }
    this.father = father

    this.fontTextbox = $(document.createElement('textbox'))
    this.fontTextbox.attr('style','position:absolute; top:15px;left:400px; border:0.5px solid #000000;width:25px;height:25px;')
    this.fontTextbox.attr('id', 'courseFont' + this.numberName)
    this.fontTextbox.attr('name', 'courseFont' + this.numberName)
    this.fontTextbox.text('9')
    this.fontTextbox.attr('contentEditable',true)

    this.questionTextbox = $(document.createElement('textarea'))
    this.questionTextbox.attr('style','position:absolute; border:0.5px solid #000000;width: 400px;height: 50px;resize: none;')
    this.questionTextbox.attr('id','questionWording' + this.numberName)
    this.questionTextbox.attr('name','questionWording' + this.numberName)
    this.questionTextbox.attr('contentEditable',true)
    this.questionTextbox.keyup(this.questionChanged.bind(this))    

    this.div = $(document.createElement('div'))
    this.div.attr('id', 'question' + this.numberName)
    this.div.attr('name', 'question' + this.numberName)
    this.div.attr('style','position:absolute; top: ' + String(this.number*50) + 'px;')
    this.div.append(this.questionTextbox)
    this.div.append(this.fontTextbox)

    if (question != null){
        this.setQuestion(question)
    }
    this.question = question

    this.ready = true
    this.changed = false 
    this.showState()
}

/**
 * Shows the QuestionBox as red if not ready and as green if changed.
 */
QuestionBox.prototype.showState = function(){
    if (!this.ready){
        color = '#FE2E2E'
    } else if (this.changed) {
        color = '#00FF00'
    } else {
        color = '#FFFFFF'
    }
    this.questionTextbox.css("background-color",color)
}

/**
 * Stores the content of this questionTextbox as a new question in the database.
 * @param idAnswerType
    *      The database id of the answerType to be related to the new question.
 */
QuestionBox.prototype.store = function(idAnswerType){
    get = new XMLHttpRequest()
    get.open( "GET", 'storeQuestions/?' + $.param({idAnswerType: idAnswerType, questionWording: this.questionTextbox.val()}), false)
    get.send(null)
    var idQuestion = parseInt(get.responseText)
    question = new Question(questionWording, idQuestion, idAnswerType)
    this.setQuestion(question)
    this.father.optionsDiv.children().detach() //Just to prevent multiple questions from beeing created.

}

/**
 * Is to be called if questionTextbox changes, it compares the questionTextbox
 * content with the question's questionWording. If it is diferent and not empy
 * marks this QuestionBox as not ready and show a list of question that match this
 * questionWording, if it is empty, set  this course as null.
 */
QuestionBox.prototype.questionChanged = function(){
    if (this.question != null){
        questionWording = this.question.questionWording
    } else {
        questionWording = ''
    }

    if (this.questionTextbox.val() != questionWording){
        if (this.questionTextbox.val() == ''){
            this.setQuestion(null)
        } else {
            this.father.showQuestionList(this.questionTextbox.val(), this)
            this.ready = false
        }
    } else {
        this.ready = true
    }
    this.showState()
}

/**
 * Set the given question as this object question, also changes this
 * questionTextbox and other parameters to fit with the new question. This marks
 * the questioBox as ready and changed.
 * @param question
    *      The question to be placed in this object.
 */
QuestionBox.prototype.setQuestion = function(question){
    if (question != this.question){
        if (question != null){
            this.questionTextbox.val(question.questionWording)
        } else {
            this.questionTextbox.val('')
        }
        this.question = question
        this.changed = true
        this.ready = true
        this.showState()
    }
    this.father.showQuestionnaire()
}

/**
 * Returns a dictionary containig the data of this object with the keys:
 * questionWording, idQuestion, idAnswerType, font and questionIndex.
 */
QuestionBox.prototype.getData = function(){
    if (this.question != null){
        data = {
            questionWording: this.question.questionWording, /**.replace(/;/g,'%3B'),*/
            idQuestion: this.question.idQuestion,
            idAnswerType: this.question.idAnswerType,
            font: this.fontTextbox.text(),
            questionIndex: this.number
        }
    } else {
        data = {
            questionWording: null, 
            idQuestion: null,
            idAnswerType: null,
            font: this.fontTextbox.text(),
            questionIndex: this.number
        }
    }
    return data
}
