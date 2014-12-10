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
	labelSizeOffers.attr('style','height: 50px; width:400; color:#b72d2d;')
    if (this.encodedCourses.length > 0){
        var encodedDiv = new $(document.createElement('div')) 
        encodedDiv.attr('style','height: 300px; overflow-y: scroll;') // para adicionar
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
        var button3 = new $(document.createElement('button'))
        button3.text('Todos')
        button3.mousedown(function(){
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
        button3.attr('style','')
		button3.attr('class','oval-minibutton')   //botao 3
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
        buttonRemove.text('Remover selecionados')
        buttonRemove.attr('style','width:180px;') //remove
		buttonRemove.attr('class','oval-minibutton')
        
        
    }
   
    if (this.listedCourses.length > 0){ 
        var listedDiv = new $(document.createElement('div')) 
        listedDiv.attr('style','float: left; height: 300px; overflow-y: scroll;') //adicionados
        for (var i in this.listedCourses){
            listedDiv.append(this.listedCourses[i].getHTML())
        }
        var button = new $(document.createElement('button'))
        button.text('Todos')
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
        button.attr('style','float: top') // button 1
		button.attr('class','oval-minibutton')
        

        var button2 = new $(document.createElement('button'))
        button2.text('Adicionar')
	
        controller = this
        button2.mousedown(function(){
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
        button2.attr('style','') //button 2
	button2.attr('class','oval-minibutton')
	$('#encoded').attr('style', 'width:100%;')	
        this.div.append(listedDiv)
		this.div.append(encodedDiv)
		this.div.append(button)
		this.div.append(button2)
		this.div.append(button3)
		this.div.append(buttonRemove)
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
    this.div.html('<span style="" >Trabalhando...</span>')
    get = new XMLHttpRequest()
    get.open( "GET", 'store/?json=' + JSON.stringify({idOpticalSheet: this.idOpticalSheet, idTimePeriod:this.idTimePeriod, idOffers: finalOffers}), false)
    get.send(null)
    this.loadEncoding()
}

Controller.prototype.removeOffers = function(offersToKeep){
    this.div.empty()
    this.div.html('<span style="" >Trabalhando...</span>')
    get = new XMLHttpRequest()
    get.open( "GET", 'store/?json=' + JSON.stringify({idOpticalSheet: this.idOpticalSheet, idTimePeriod:this.idTimePeriod, idOffers: offersToKeep}), false)
    get.send(null)
    this.loadEncoding()
}
