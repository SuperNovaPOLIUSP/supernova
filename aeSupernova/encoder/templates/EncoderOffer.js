function Offer(idOffer, professorName, classNumber){
    this.idOffer = idOffer
    this.professorName = professorName 
    this.classNumber = classNumber
}

Offer.prototype.getHTML = function(){
    var div = new $(document.createElement('div'))
    var span = new $(document.createElement('span'))
    span.text('Turma:' + this.classNumber + ' - Professor(a) - ' + this.professorName)
    span.attr('style', 'font-size:10px')
    var input = new $(document.createElement('input'))
    input.attr('type','checkbox')
    input.val(this.idOffer)
    div.append(input)
    div.append(span)
    return div
}
