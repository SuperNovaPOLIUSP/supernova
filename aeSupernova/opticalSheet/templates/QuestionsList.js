/**
  * class QuestionsList
  * A object to show the options of questions to put in a questionBox.
  */
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 
    /**
     * A List of all the database's questions in form of Question objects.
     */
    //questions 
    /**
     * A subgroup of questions list, only with the questions to be shown.
     */
    //listedQuestions 

/**
 * Initialization method.
 */
function QuestionsList(){
    this.div = $(document.createElement('div'))
    this.div.attr('id', 'QuestionsList')
    this.div.attr('name', 'QuestionsList')
    this.questions = new Array()
    this.getQuestions()
    this.listedQuestions = this.questions
}

/**
 * Send a GET to /opticalSheet/getQuestions/ the response is a list with all the
 * database's question in form of dicts, then they are converted in Question
 * objects and placed in the questions list.
 */
QuestionsList.prototype.getQuestions = function(){
    get = new XMLHttpRequest()
    get.open( "GET", 'getQuestions/', false)
    get.send(null)
    var questionsData = JSON.parse(get.responseText)
    this.questions = new Array()
    for (var i in questionsData){
        question = new Question(questionsData[i]['questionWording'], questionsData[i]['idQuestion'], questionsData[i]['idAnswerType'])
        this.questions[i] = question
    }
}

/**
 * Searches in the questions list for questions with questionWording like the
 * given, those questions are placed in the listedQuestions list.
 * @param questionWording
    *      Part of the questionWording of the wanted question.
 */
QuestionsList.prototype.search = function(questionWording){
    this.listedQuestions = new Array()
    for (var i in this.questions){
        if (this.questions[i]['questionWording'].indexOf(questionWording) != -1){
            this.listedQuestions.push(this.questions[i])
        }
    }
}

/**
 * Shows all the answerTypes for the user to chose one for the new question to be
 * created.
 * @param questionBox
    *      The questionBox that requested this method.
 * @param answerTypes
    *      A list of all possible answerTypes
 */
QuestionsList.prototype.createQuestion = function(questionBox, answerTypes){
    questionWording = questionBox.questionTextbox.val()
    this.div.children().detach()
    span = $(document.createElement('span'))
    span.text('seleção de questão para a linha ' + String(questionBox.number + 1) + ':')
    this.div.append(span)
    select = $(document.createElement('div'))
    select.attr('size',12)
    select.attr('style','width: 1000px;height: 300px; overflow-y: scroll;')
    this.div.append(select)
    for (var i in answerTypes){
            var answerTypeDiv = new $(document.createElement('div'))
            var answerTypeSpan = new $(document.createElement('span'))
            answerTypeSpan.text(answerTypes[i].name + '(')
            for (var letter in answerTypes[i].alternativeMeaning){
                answerTypeSpan.text( answerTypeSpan.text() + ';' + letter + ':' + answerTypes[i].alternativeMeaning[letter])
            }
            answerTypeSpan.text( answerTypeSpan.text() + ')')
            var selectButton = new $(document.createElement('button'))
            selectButton.text('select')
            selectButton.mousedown(questionBox.store.bind(questionBox, answerTypes[i].idAnswerType))
            selectButton.attr('style', 'float: right;')
            answerTypeDiv.append(answerTypeSpan)
            answerTypeDiv.append(selectButton)
            answerTypeDiv.attr('style', 'height: 50px; border:1px solid black;')
            select.append(answerTypeDiv)
    }
}

/**
 * Show the listedQuestions for the user, so he can select one of them to be placed
 * in the given questionBox.
 * @param questionBox
    *      QuestionBox that called this method.
 */
QuestionsList.prototype.showList = function(questionBox){
    this.div.children().detach()
    span = $(document.createElement('span'))
    span.text('seleção de questão para a linha ' + String(questionBox.number + 1) + ':')
    this.div.append(span)
    select = $(document.createElement('div'))
    select.attr('size',12)
    select.attr('style','width: 1000px;height: 300px; overflow-y: scroll;')
    this.div.append(select)
    for (var i in this.listedQuestions){
            var questionsDiv = new $(document.createElement('div'))
            var questionSpan = new $(document.createElement('span'))
            questionSpan.text(this.listedQuestions[i].questionWording)
            var addButton = new $(document.createElement('button'))
            addButton.text('add')
            addButton.mousedown(questionBox.setQuestion.bind(questionBox, this.listedQuestions[i]))
            addButton.attr('style', 'float: right;')
            questionsDiv.append(questionSpan)
            questionsDiv.append(addButton)
            questionsDiv.attr('style', 'height: 75px; border:1px solid black;')
            select.append(questionsDiv)
    }
}
