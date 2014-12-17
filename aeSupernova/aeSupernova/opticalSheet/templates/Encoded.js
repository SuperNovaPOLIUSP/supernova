/**
  * class Encoded
  * Is used to let the user select and change the encoding, beenig used if this is
  * to be an encoded opticalSheet.
  */
    /**
     * A list of all the encodings in the database that belong to the same timePeriod
     * as chosen by the user. Each one is represented as a dict with the keys:
     * encodingName and idOpticalSheet.
     */
    //encodings 
    /**
     * A html div that holds all HTML elements of this object.
     */
    //div 
    /**
     * The opticalSheet object that this encoding belong to.
     */
    //opticalSheet 
    /**
     * A boolean representing that this encoding is ready to be stored.
     */
    //okToSave 
    /**
     * A boolean representing that this encoding is ready to be printed.
     */
    //okToPrint 
    /**
     * A boolean representing that this encoding was changed.
     */
    //changed 
    /**
     * A boolean representing that this encoding was set.
     */
    //set 


/**
 * Initialization method.
 * @param opticalSheet
    *      
 */
function Encoded(opticalSheet){
    this.encodings = new Array()
    this.div = $(document.createElement('div'))
    this.div.attr('id', 'encoded')
    this.div.attr('name', 'encoded')
    this.div.attr('style','position:absolute; top:100px; left:700px;')
    this.opticalSheet = opticalSheet
    this.okToSave = false
    this.okToPrint = false
    this.changed = false
    this.set = false
}

/**
 * Send a GET to opticalSheet/getEncodings/ with the idTimePeriod, the response is
 * this class encodings list. From this list is created a html element select where
 * each encoding is placed as a option, and this select is placed in this class's
 * div.
 * @param idTimePeriod
    *      The database id of the timePeriod selected by the user.
 */
Encoded.prototype.getEncodings = function(idTimePeriod){
    get = new XMLHttpRequest()
    get.open( "GET", 'getEncodings/?idTimePeriod=' + idTimePeriod, false)
    get.send(null)
    var encodings = JSON.parse(get.responseText)
    var select = $(document.createElement('select'))
    var option = $(document.createElement('option'))
    option.text = ''
    option.val = 0
    select.append(option)
    for (var i in encodings){
        var option = $(document.createElement('option'))
        option.text(encodings[i]['encodingName'])
        option.val(encodings[i]['idOpticalSheet'])
        select.append(option)
    }
    select.change(this.changeEncoding.bind(this))
    this.div.append(select)
    this.changed = false
    this.set = false
}

/**
 * Check and set the okToSave and okToPrint bool.
 */
Encoded.prototype.checkState = function(){
    if (!this.changed && this.set){
        this.okToPrint = true
    } 
    if (this.changed){
        this.okToPrint = false
    }
    if (!this.changed && !this.set){
        this.okToSave = false
    }
    if (this.changed || this.set){
        this.okToSave = true
    }
}

/**
 * This is called onChange of the select created in getEncodings(). This loads the
 * opticalSheet to the encoding selectet, and set the changed as true.
 */
Encoded.prototype.changeEncoding = function(){
    this.opticalSheet.findOpticalSheetById(this.div.children('select').eq(0).val())
    this.changed = true //Need to store first
}

/**
 * This function is used when the opticalSheet already have a defined encoding, in
 * this case the encoding is presented as a span and a button that allows the user
 * to disassociate this encoding to the cycle, term selected.
 * @param encodingName
    *      The name of the encoding to be set.
 */
Encoded.prototype.setEncoding = function(encodingName){
    this.div.children().detach()
    var span = $(document.createElement('span'))
    span.text(encodingName)
    this.div.append(span)
    var button = $(document.createElement('button'))
    button.text('remove this Cycle from this OpticalSheet')
    button.mousedown(this.opticalSheet.removeCycleFromOpticalSheet.bind(this.opticalSheet))
    this.div.append(button)
    this.set = true
    //for (var i in this.div.children('select').eq(0).children('option')){
    //    if (this.div.children('select').eq(0).children('option').eq(i).val() == idOpticalSheet){
    //        this.div.children('select').eq(0).children('option').eq(i).attr('selected', 'selected');
    //    }
    //}
}

/**
 * Returns the name on the span created in setEncoding().
 */
Encoded.prototype.getData = function(){
    return this.div.children('span').eq(0).text()
}
