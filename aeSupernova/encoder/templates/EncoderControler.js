function Controller(){
    this.idOpticalSheet = null
    this.listedCourses = new Array()
    this.encodedCourses = new Array()
    this.div = new $(document.createElement('div'))
}

Controller.prototype.loadCourses = function(coursesData){
    courses = new Array()
    for (var i in coursesData){
        course = new Course(coursesData[i]['courseCode'], coursesData[i]['courseName'], coursesData[i]['offers'])
        courses.push(course)
    }
    return courses
}

Controller.prototype.loadEncoding = function(){
    if (this.idOpticalSheet != null){
        get = new XMLHttpRequest()
        get.open( "GET", 'loadEncoding/?' + $.param({idOpticalSheet: this.idOpticalSheet, idTimePeriod: this.idTimePeriod}), false)
        get.send(null)
        coursesData = JSON.parse(get.responseText)
        this.encodedCourses = this.loadCourses(coursesData)
        this.showEncoding()
    }
}

Controller.prototype.showPossibleOffers = function(idCycle, term){
    get = new XMLHttpRequest()
    get.open( "GET", "showPossibleOffers/?" + $.param({idOpticalSheet: this.idOpticalSheet, idTimePeriod: this.idTimePeriod, idCycle: idCycle, term: term}), false)
    get.send(null)
    coursesData = JSON.parse(get.responseText)
    this.listedCourses = this.loadCourses(coursesData)
    this.showEncoding() 
}

Controller.prototype.showEncoding = function(){
    this.div.empty()
	var labelSizeOffers = new $(document.createElement('p'))
	labelSizeOffers.attr('style','position:absolute; top:500px; left:130px; height: 100px; width:400; color:red;')
    if (this.encodedCourses.length > 0){
        var encodedDiv = new $(document.createElement('div')) 
        encodedDiv.attr('style','position:absolute; top:100px; left:100px; height: 300px; width:400; overflow-y: scroll;')
        for (var i in this.encodedCourses){
            encodedDiv.append(this.encodedCourses[i].getHTML())
        }
        var totalOffers = new Array()
        for (var i in this.encodedCourses){
        	for (var j in this.encodedCourses[i].offers){
            	totalOffers.push(this.encodedCourses[i].offers[j].idOffer)
        	}
    	}
        labelSizeOffers.text("Número de Offers: " + totalOffers.length.toString())
        var button = new $(document.createElement('button'))
        button.text('flip All')
        button.mousedown(function(){
           if (encodedDiv.find('input').eq(0).attr('checked')){
                encodedDiv.find('input').each(function(){
                    $(this).attr('checked', false);
                })
            } else {
                encodedDiv.find('input').each(function(){
                    $(this).attr("checked", true);
                })
            }
        })
        button.attr('style','position:absolute; top:400px; left:150px;')
        this.div.append(button)
        this.div.append(labelSizeOffers)
        var buttonRemove = new $(document.createElement('button'))
        controller = this
        buttonRemove.mousedown(function(){
            offersToKeep = new Array()
            encodedDiv.find('input').each(function(){
            	if (!($(this).attr('checked'))){
                	if ($(this).val() != '0'){ 
                        offersToKeep.push($(this).val())
                    }
                }
            })
            controller.removeOffers(offersToKeep)
        })
        buttonRemove.text('removeSelected')
        buttonRemove.attr('style','position:absolute; top:400px; left:230px;')
        this.div.append(buttonRemove)
        this.div.append(encodedDiv)
    }
   
    if (this.listedCourses.length > 0){ 
        var listedDiv = new $(document.createElement('div')) 
        listedDiv.attr('style','position:absolute; top:100px; left:700px; height: 300px; width:400; overflow-y: scroll;')
        for (var i in this.listedCourses){
            listedDiv.append(this.listedCourses[i].getHTML())
        }
        var button = new $(document.createElement('button'))
        button.text('flip All')
        button.mousedown(function(){
           if (listedDiv.find('input').eq(0).attr('checked')){
                listedDiv.find('input').each(function(){
                    $(this).attr('checked', false);
                })
            } else {
                listedDiv.find('input').each(function(){
                    $(this).attr("checked", true);
                })
            }
        })
        button.attr('style','position:absolute; top:400px; left:750px;')
        this.div.append(button)

        var button = new $(document.createElement('button'))
        button.text('addSelected')
        controller = this
        button.mousedown(function(){
            newOffers = new Array()
            listedDiv.find('input').each(function(){
                if ($(this).attr('checked')){
                    if ($(this).val() != '0'){ 
                        newOffers.push($(this).val())
                    }
                }
            })
            controller.storeOffers(newOffers)
        })
        button.attr('style','position:absolute; top:400px; left:850px;')
        this.div.append(button)
        this.div.append(listedDiv)
    }

}

Controller.prototype.storeOffers = function(newOffers){
    finalOffers = new Array()
    for (var i in newOffers){
        finalOffers.push(newOffers[i])
    }
    for (var i in this.encodedCourses){
        for (var j in this.encodedCourses[i].offers){
            finalOffers.push(this.encodedCourses[i].offers[j].idOffer)
        }
    }
    this.div.empty()
    this.div.html('<span style="position:absolute; left:200px; top:200px" >Trabalhando...</span>')
    get = new XMLHttpRequest()
    get.open( "GET", 'store/?json=' + JSON.stringify({idOpticalSheet: this.idOpticalSheet, idTimePeriod:this.idTimePeriod, idOffers: finalOffers}), false)
    get.send(null)
    this.loadEncoding()
}

Controller.prototype.removeOffers = function(offersToKeep){
    this.div.empty()
    this.div.html('<span style="position:absolute; left:200px; top:200px" >Trabalhando...</span>')
    get = new XMLHttpRequest()
    get.open( "GET", 'store/?json=' + JSON.stringify({idOpticalSheet: this.idOpticalSheet, idTimePeriod:this.idTimePeriod, idOffers: offersToKeep}), false)
    get.send(null)
    this.loadEncoding()
}
