/**
  * class OpticalSheet
  * 
  */
    /**
     * The databse id of the cycle related to this opticalSheet.
     */
    //idCycle;
    /**
     * The term of the relatation between the cycle and the opticalSheet.
     */
    //term;
    /**
     * The database id of this opticalSheet's timePeriod.
     */
    //idTimePeriod;
    /**
     * A list of questionnaire objects that represent this opticalSheet's
     * questionnaires.
     */
    //questionnaires;
    /**
     * The questionnaire of the array questionnaires that is visible to the user.
     */
    //useQuestionnaire = -1;
    /**
     * A html element div that belongs to the body of the html code and is a general
     * area to be used by the objects.
     */
    //optionsDiv;
    /**
     * A div that contains all of the opticalSheet's related buttons.
     */
    //buttons;
    /**
     * This opticalSheet's positions object.
     */
    //positions;
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div;
    /**
     * A div with the buttons to the user select id the new opticalSheet is to be
     * encoded or not.
     */
    //initialButtons;
    /**
     * This opticalSheets Columns.
     */
    //columns;
    /**
     * True if the opticalSheet is encoded.
     */
    //encoded;
    /**
     * The database id of this opticalSheet, if this is a new opticalSheet the
     * idOpticalSheet is null.
     */
    //idOpticalSheet;

/**
 * 
 * @param optionsDiv
    *      
 * @param idTimePeriod
    *      
 * @param idCycle
    *      
 * @param term
    *      
 */
function OpticalSheet(optionsDiv, idTimePeriod, idCycle, term){
    this.idCycle = parseInt(idCycle)
    this.term = parseInt(term)
    this.idTimePeriod = parseInt(idTimePeriod)
    this.questionnaires = new Array()
    this.usedQuestionnaire = -1
    this.optionsDiv = optionsDiv

    this.buttons = $(document.createElement('div'))
    this.buttons.attr('id', 'buttons')
    this.buttons.attr('name', 'buttons')

    storeButton = $(document.createElement('button'))
    storeButton.attr('style','position:absolute; top:600px; left:800px; display:block;')
    storeButton.text('store')
    storeButton.mousedown(this.store.bind(this))

    printOpticalSheetButton = $(document.createElement('button'))
    printOpticalSheetButton.attr('style','position:absolute; top:600px; left:1000px; display:block;')
    printOpticalSheetButton.text('print OpticalSheet')
    printOpticalSheetButton.mousedown(this.printOpticalSheet.bind(this))
    
    printAMCButton = $(document.createElement('button'))
    printAMCButton.attr('style','position:absolute; top:600px; left:1150px; display:block;')
    printAMCButton.text('print AMC')
    printAMCButton.mousedown(this.printAMC.bind(this))

    printQualitativeQuestionnaireButton = $(document.createElement('button'))
    printQualitativeQuestionnaireButton.attr('style','position:absolute; top:600px; left:870px; display:block;')
    printQualitativeQuestionnaireButton.text('print Qualitative')
    printQualitativeQuestionnaireButton.mousedown(this.printQualitativeQuestionnaire.bind(this))

    copyQuestionnaireButton = $(document.createElement('button'))
    copyQuestionnaireButton.attr('style','position:absolute; top:650px; left:10px; display:block;')
    copyQuestionnaireButton.text('copyQuestionnaire')
    copyQuestionnaireButton.mousedown(this.showCopyQuestionnaire.bind(this))

    createNewAssessmentButton = $(document.createElement('button'))
    createNewAssessmentButton.attr('style', 'position:absolute; top:650px; left:200px; display:block;')
    createNewAssessmentButton.text('Create assessment')
    createNewAssessmentButton.mousedown(this.createNewAssessment.bind(this))

    nextAssessmentButton = $(document.createElement('button'))
    nextAssessmentButton.attr('style', 'position:absolute; top:650px; left:300px; display:block;')
    nextAssessmentButton.text('Next assessment')
    nextAssessmentButton.mousedown(this.nextAssessment.bind(this))

    this.buttons.append(nextAssessmentButton)
    this.buttons.append(createNewAssessmentButton)
    this.buttons.append(printOpticalSheetButton)
    this.buttons.append(printAMCButton)
    this.buttons.append(printQualitativeQuestionnaireButton)
    this.buttons.append(storeButton)
    this.buttons.append(copyQuestionnaireButton)

    this.positions = new Positions()

    this.div = $(document.createElement('div'))
    this.div.attr('id', 'opticalSheet')
    this.div.attr('name', 'opticalSheet')
    this.div.attr('style','position:absolute; top:50px; left:0px;')
}

/**
 * Start a new opticalSheet, setting the questionnaires and columns to null and a
 * buttons to chose if it is encoded or not.
 */
OpticalSheet.prototype.newOpticalSheet = function(){
    encodedButton = $(document.createElement('button'))
    encodedButton.text('encoded')
    encodedButton.mousedown(this.createNewOpticalSheet.bind(this, true))
    nonEncodedButton = $(document.createElement('button'))
    nonEncodedButton.text('nonEncoded')
    nonEncodedButton.mousedown(this.createNewOpticalSheet.bind(this, false))
    this.initialButtons = $(document.createElement('div'))
    this.initialButtons.attr('style','position:absolute; top:50px; left:600px; display:block;')
    this.initialButtons.append(encodedButton)
    this.initialButtons.append(nonEncodedButton)
    this.columns = null
    this.questionnaires = new Array()
    this.usedQuestionnaire = -1
}

/**
 * Sends a get to /opticalSheet/findOpticalSheetById/ with the given
 * idOpticalSheet, the response is a JSON with all the data of the chosen
 * opticalSheet. This data is then passed to the loadOpticalSheet method.
 * @param idOpticalSheet
    *      The id of the wanted opticalSheet
 */
OpticalSheet.prototype.findOpticalSheetById = function(idOpticalSheet){
    get = new XMLHttpRequest()
    get.open( "GET", 'findOpticalSheetById/?' + $.param({idOpticalSheet : idOpticalSheet}), false)
    get.send(null)
    this.loadOpticalSheet(JSON.parse(get.responseText))
}

/**
 * Sends a get to /opticalSheet/findOpticalSheetById/ with this objects
 * idTimePeriod, idCycle and term, the response is a JSON with all the data of the
 * opticalSheet fiting this parameters, if there is not exactly one the response is
 * the number of founds opticalSheet. This data is then passed to the
 * loadOpticalSheet method.
 */

OpticalSheet.prototype.findOpticalSheetByTimePeriod_Cycle_Term = function(){
    get = new XMLHttpRequest()
    get.open( "GET", 'findOpticalSheetByTimePeriod_Cycle_Term/?' + $.param({idCycle : this.idCycle, term : this.term, idTimePeriod : this.idTimePeriod}), false)
    get.send(null)
    this.loadOpticalSheet(JSON.parse(get.responseText))
}

/**
 * If the opticalSheetData is a int alert a mensage showing the number of
 * opticalSheets found. Else the opticalSheets page is loaded with this data.
 * @param opticalSheetData
    *      The response of the findOpticalSheet methods of the server.
 */

OpticalSheet.prototype.loadOpticalSheet = function(opticalSheetData){
    if (typeof(opticalSheetData) != 'object'){
        if (opticalSheetData != 0 ){
            alert('erro achou ' + opticalSheetData + ' folhas Oticas')
        }
        else {    
            this.newOpticalSheet() 
        }
    } else {
        this.encoded = 'encodingName' in opticalSheetData 
        this.surveyType = opticalSheetData['surveyType']
        this.idOpticalSheet = opticalSheetData['idOpticalSheet']
        this.loadQuestionnaires(opticalSheetData['surveys'])
        if (!this.encoded){
            this.loadColumns(opticalSheetData['fields'])
        } else {
            this.loadEncoding(opticalSheetData['encodingName'])
        }
    }
    this.showOpticalSheet()
}

/**
 * Send a post to the /opticalSheet/store/ with the return of this.getData() and
 * alert its return.
 */
OpticalSheet.prototype.store = function(){
    okToSaveQuestionnaire = true
    for (var i in this.questionnaires){
        this.questionnaires[i].checkState()
        if (!this.questionnaires[i].okToSave){
            okToSaveQuestionnaire = false
        }
    }
    this.columns.checkState()
    if (okToSaveQuestionnaire && this.columns.okToSave){
        opticalSheetData = this.getData()
        opticalSheet = this //JQuery doesn't know how to work with 'this' inside the return function
        this.showWorking()
        $.post('store/', {json: JSON.stringify(opticalSheetData), csrfmiddlewaretoken: '{{ csrf_token }}'}).done(function(response,status){
            alert(response)
            opticalSheet.findOpticalSheetByTimePeriod_Cycle_Term()
        }).fail(function(){
            alert('deu algum problema')
            opticalSheet.showOpticalSheet()
        })
    } else {
        alert('OpticalSheet is not ready to store!')
    }
}

/**
 * Sends a post to /opticalSheet/printOpticalSheet/ with the needed data, if the
 * post is successful open a new tab with the address
 * /opticalSheet/getPrintedOpticalSheet/ with the needed data to download the
 * opticalSheet to the user.
 */
OpticalSheet.prototype.printOpticalSheet = function(){
    this.questionnaires[this.usedQuestionnaire].checkState() 
    this.columns.checkState()
    if (this.questionnaires[this.usedQuestionnaire].okToPrint && this.columns.okToPrint){
        opticalSheetData = this.getData()
        opticalSheetData['survey'] = this.questionnaires[this.usedQuestionnaire].getData() //for this one only the choseQuestionnaire is important
        term = this.term //JQuery doesn't know how to work with 'this' inside the retunr function
        idCycle = this.idCycle
        idTimePeriod = this.idTimePeriod
        downloadType = opticalSheetData['positions']['downloadType']
        $.post('printOpticalSheet/', {json: JSON.stringify(opticalSheetData), csrfmiddlewaretoken: '{{ csrf_token }}'}).done(function(data,status){
            window.open('getPrintedOpticalSheet/?' + $.param({idTimePeriod: idTimePeriod, idCycle: idCycle, term: term, downloadType: downloadType}),'_blank')
        }).fail(function(){alert('deu problema')})
        //window.open('getPrintedOpticalSheet/?' + $.param({idTimePeriod: this.idTimePeriod, idCycle: this.idCycle, term: this.term}),'_blank')
    } else {
        alert('OpticalSheet is not ready to print!'
)
    }
}

/**
 * Sends a post to /opticalSheet/printAMC/ with the needed data, if the
 * post is successful open a new tab with the address
 * /opticalSheet/getPrintedAMC/ with the needed data to download the
 * opticalSheet to the user.
 */
OpticalSheet.prototype.printAMC = function(){
    this.questionnaires[this.usedQuestionnaire].checkState() 
    this.columns.checkState()
    if (this.questionnaires[this.usedQuestionnaire].okToPrint && this.columns.okToPrint){
        AMCData = this.getData()
        AMCData['survey'] = this.questionnaires[this.usedQuestionnaire].getData() //for this one only the choseQuestionnaire is important
        term = this.term //JQuery doesn't know how to work with 'this' inside the retunr function
        idCycle = this.idCycle
        idTimePeriod = this.idTimePeriod
        downloadType = AMCData['positions']['downloadType']
        $.post('printAMC/', {json: JSON.stringify(AMCData), csrfmiddlewaretoken: '{{ csrf_token }}'}).done(function(data,status){
            window.open('getPrintedAMC/?' + $.param({idTimePeriod: idTimePeriod, idCycle: idCycle, term: term, downloadType: downloadType}),'_blank')
        }).fail(function(){alert('deu problema no AMC')})
        //window.open('getPrintedAMC/?' + $.param({idTimePeriod: this.idTimePeriod, idCycle: this.idCycle, term: this.term}),'_blank')
    } else {
        alert('AMC is not ready to print!'
)
    }
}

/**
 * Sends a post to /opticalSheet/printQualitativeQuestionnaire/ with the needed
 * data, if the post is successful open a new tab with the address
 * /opticalSheet/getPrintedQualitativeQuestionnaire/ with the needed data to
 * download the qualitativeQuestionnaire to the user.
 */
OpticalSheet.prototype.printQualitativeQuestionnaire = function(){
    this.questionnaires[this.usedQuestionnaire].checkState() 
    this.columns.checkState()
    positionData = this.positions.getData()
    if (this.questionnaires[this.usedQuestionnaire].okToPrint && this.columns.okToPrint){
        qqData = {idOpticalSheet: this.idOpticalSheet, idTimePeriod: this.idTimePeriod, idCycle: this.idCycle, term: this.term, numberOfAnswerLines: positionData['numberOfLines'], qualitativeQuestionnaireType: positionData['qualitativeQuestionnaireType'], downloadType: positionData['downloadType']}
        
        term = this.term //JQuery doesn't know how to work with 'this' inside the retunr function
        idCycle = this.idCycle
        idTimePeriod = this.idTimePeriod
        downloadType = positionData['downloadType']
        $.post('printQualitativeQuestionnaire/', {json: JSON.stringify(qqData), csrfmiddlewaretoken: '{{ csrf_token }}'}).done(function(data,status){
            window.open('getPrintedQualitativeQuestionnaire/?' + $.param({idTimePeriod: idTimePeriod, idCycle: idCycle, term: term, downloadType: downloadType}),'_blank')
        }).fail(function(){alert('deu problema')})
    } else {
        alert('OpticalSheet is not ready to print!')
    }
}

/**
 * Gets all the data of the opticalSheet and returns in the form of a dict.
 */
OpticalSheet.prototype.getData = function(){
    surveysData = new Array()
    for (var i in this.questionnaires){
        surveysData.push(this.questionnaires[i].getData())
    }
    opticalSheetData = {
        idOpticalSheet: this.idOpticalSheet,
        encoded: this.encoded,
        surveyType: this.surveyType,
        fields: this.columns.getData(),
        idCycle: this.idCycle,
        term: this.term,
        idTimePeriod: this.idTimePeriod,
        surveys: surveysData,
        positions: this.positions.getData()
    }
    return opticalSheetData
}

/**
 * Starts a new empty opticalSheet, creating a first assessment questionnaire and a
 * empty columns if it is not encoded or a select with the options of encoding.
 * @param encoded
    *      Booleand showing if this is to be an encoded opticalSheet.
 */
OpticalSheet.prototype.createNewOpticalSheet = function(encoded){
    if (!encoded){
        this.columns = new Columns(optionsDiv, this.idTimePeriod, this.idCycle, this.term)
        this.surveyType = 'Tradicional'
    } else {
        this.columns = new Encoded(this)
        this.columns.getEncodings(this.idTimePeriod)
    }
    this.encoded = encoded
    this.idOpticalSheet = null
    questionnaire = new Questionnaire(this.optionsDiv, null, 1)
    this.usedQuestionnaire = 0 
    this.questionnaires.push(questionnaire)
    this.showOpticalSheet()
}

/**
 * Set this opticalSheet's columns parameter to a new Encoded object and run the
 * encoded method setEncoding.
 * @param encodingName
    *      This opticalSheet's encoding name.
 */
OpticalSheet.prototype.loadEncoding = function(encodingName){
    this.columns = new Encoded(this)
    this.columns.setEncoding(encodingName)
}

/**
 * Set this opticalSheet's columns parameter to a new Columns and load the data in
 * the fieldData to the new Columns.
 * @param fieldData
    *      A list of dicts with the keys: courseCode, courseName, courseAbbreviation,
    *      idCourse and courseIndex.
 */
OpticalSheet.prototype.loadColumns = function(fieldsData){
    this.columns = new Columns(optionsDiv, this.idTimePeriod, this.idCycle, this.term)
    for (var i in fieldsData){
        course = new Course(fieldsData[i]['courseCode'], fieldsData[i]['courseName'], fieldsData[i]['courseAbbreviation'], fieldsData[i]['idCourse'], fieldsData[i]['idsOffer'])
        this.columns.loadColumn(course, fieldsData[i]['courseIndex'])
    }
}

/**
 * Change the assessment to be showed in the site to the next assessment, if it is
 * already in the last assessment goes to the first.
 */
OpticalSheet.prototype.nextAssessment = function(){
    for (var i in this.questionnaires){
        if (i == (this.usedQuestionnaire)){
            if (i == (this.questionnaires.length - 1)){
                this.usedQuestionnaire = 0
            } else {
                this.usedQuestionnaire = parseInt(i) + 1
            }
            break
        }
    }
    this.showOpticalSheet()
}

/**
 * Create e new assessment for this opticalSheet, with the next assessmentNumber
 * avaliable.
 */
OpticalSheet.prototype.createNewAssessment = function(){
    this.createQuestionnaire(this.questionnaires.length + 1)
}

/**
 * Creates a new Questionnaire object with the given assessmentNumber, place in the
 * questionnaires list and showes it in the page.
 * @param assessmentNumber
    *      The assessmentNumber of the new questionnaire.
 */
OpticalSheet.prototype.createQuestionnaire = function(assessmentNumber){
    var questionnaire = new Questionnaire(this.optionsDiv, null, assessmentNumber)
    this.usedQuestionnaire = assessmentNumber - 1
    this.questionnaires.push(questionnaire)
    this.showOpticalSheet()
}

/**
 * Creates and put in the questionnaires array new Questionnaire objects with the
 * questions and data of the given data.
 * @param surveysData
    *      A list of dicts with the keys: idQuestionnaires, assessmentNumber, questions.
 */
OpticalSheet.prototype.loadQuestionnaires = function(surveysData){
    this.usedQuestionnaire = -1
    this.questionnaires = new Array()
    for (var i in surveysData){
        questionnaire = new Questionnaire(this.optionsDiv, surveysData[i]['idQuestionnaire'], surveysData[i]['assessmentNumber'])
        for (var j in surveysData[i]['questions']){
            questionData = surveysData[i]['questions'][j]
            question = new Question(questionData['questionWording'], questionData['idQuestion'], questionData['idAnswerType'])
            questionnaire.loadQuestion(question, questionData['questionIndex'])
        }
        this.questionnaires.push(questionnaire)
        this.usedQuestionnaire++
    }
    if (this.usedQuestionnaire == -1){ //No questionnaire was loaded
        this.createQuestionnaire(1)
    }
}

/**
 * Copy the questionnaires parameter of the chosen opticalSheet.
 * @param idOpticalSheet
    *      The id of the opticalSheet to copy the questionnaires.
 */
OpticalSheet.prototype.copyQuestionnaire = function(idOpticalSheet){
    get = new XMLHttpRequest()
    get.open( "GET", 'findOpticalSheetById/?' + $.param({idOpticalSheet : idOpticalSheet}), false)
    get.send(null)
    this.loadQuestionnaires(JSON.parse(get.responseText)['surveys'])
    this.showOpticalSheet()
}

/**
 * From the selected cycle in showCopyQuestionnaire function, this sends a GET to
 * /opticalSheet/listOldOpticalSheets/ them display the old opticalSheets for the
 * user to select from with copy the questionnaires
 */
OpticalSheet.prototype.showCopyQuestionnairesList = function(){
    get = new XMLHttpRequest()
    get.open( "GET", 'listOldOpticalSheets/?' + $.param({idCycle: $('#copyCycle').val()}), false)
    get.send(null)
    var oldOpticalSheets = JSON.parse(get.responseText)
    select = $(document.createElement('div'))
    select.attr('size',12)
    select.attr('style','position:absolute; top:30px; width: 1000px;height: 300px; overflow-y: scroll;')
    for (var i in oldOpticalSheets){
        var OODiv = new $(document.createElement('div'))
        var OOSpan = new $(document.createElement('span'))
        OOSpan.text(oldOpticalSheets[i]['term'] + ' - ' + oldOpticalSheets[i]['timePeriod'])
        var addButton = new $(document.createElement('button'))
        addButton.text('add')
        addButton.mousedown(this.copyQuestionnaire.bind(this, oldOpticalSheets[i]['idOpticalSheet']))
        addButton.attr('style', 'float: right;')
        OODiv.append(OOSpan)
        OODiv.append(addButton)
        OODiv.attr('style', 'height: 30px; border:1px solid black;')
        select.append(OODiv)
    }
    this.optionsDiv.append(select)

}

/**
 * Place in the options div selects for the user to chose from which cycle the
 * questionnaire will be copied
 */
OpticalSheet.prototype.showCopyQuestionnaire = function(){
    this.optionsDiv.children().detach()
    var div = $(document.createElement('div'))
    var cycle = $(document.createElement('select'))
    cycle.html($('#headerCycle').children().clone());
    cycle.attr('id','copyCycle')
    cycle.attr('style', 'position:absolute; top:0px; left:300px')
    cycle.hide()
    cycle.change(this.showCopyQuestionnairesList.bind(this))
    var faculty = $(document.createElement('select'))
    faculty.html($('#headerFaculty').children().clone());
    faculty.attr('id','copyFaculty')
    faculty.attr('style', 'position:absolute; top:0px; left: 0px')
    faculty.change(function(){
        var idFaculty = document.getElementById("copyFaculty").value
        $("#copyCycle").children('option').each(function(){
            $(this).hide()
        });
        $("#copyCycle").children('option').each(function(){
            if ($(this).attr('idFaculty') == idFaculty){
                $(this).show()
            }
        });
        $("#copyCycle").show();
    })
    faculty.show()
    div.append(faculty)
    div.append(cycle)
    this.optionsDiv.append(div)
    this.optionsDiv.show()
}

/**
 * Replace the content of the parameter div with the needed opticalSheet data
 */
OpticalSheet.prototype.showWorking = function(){
    this.div.children().detach()
    var span = new $(document.createElement('span'))
    span.text('Trabalhando...(isso pode demorar)')
    span.attr('style','position:absolute; top:200px; left:200px;')
    this.div.append(span)

}

/**
 * Replace the content of the parameter div with the needed opticalSheet data
 */
OpticalSheet.prototype.showOpticalSheet = function(){
    this.div.children().detach()
    if (this.columns){
        this.div.append(this.columns.div)
    } else {
        this.div.append(this.initialButtons)
    }
    if (this.usedQuestionnaire > -1){
        this.div.append(this.questionnaires[this.usedQuestionnaire].div)
    }
    this.div.append(this.positions.div)
    this.div.append(this.buttons)
}

/**
 * Sends a get to the /opticalSheet/removeCycleFromOpticalSheet/ with the
 * parameters idCycle, term and idOpticalSheet. Then calls the method
 * this.findOpticalSheetByTimePeriod_Cycle_Term().
 */
OpticalSheet.prototype.removeCycleFromOpticalSheet = function(){
    get = new XMLHttpRequest()
    get.open( "GET", 'removeCycleFromOpticalSheet/?' + $.param({idCycle: this.idCycle, term: this.term, idOpticalSheet: this.idOpticalSheet}), false)
    get.send(null)
    this.findOpticalSheetByTimePeriod_Cycle_Term() 
}
