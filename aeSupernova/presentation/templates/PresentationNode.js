function PresentationNode(url, datas, id, name){
    this.id = id
    this.name = name
    this.div = $(document.createElement('div')) 
    this.div.attr('id',id)
    this.nexts = null

    var nextsDiv = $(document.createElement('div'))
    nextsDiv.attr('style', 'margin-top:30px;')
    nextsDiv.show()
    if (url != ''){
        this.createNextNodes(url, datas)

        var button = $(document.createElement('button'))
        button.text('-')
        button.mousedown(this.close.bind(this))
        this.div.append(button)
        for (var i in this.nexts){
            nextsDiv.append(this.nexts[i].div)
        }
    } else {
        this.datas = datas
        for (var i in datas){
            //var span = $(document.createElement('span'))
            //span.text(datas[i][url]['name'])
            //nextsDiv.append(span)
            var link = new $(document.createElement('a'))
            link.text(datas[i]['course']['name'])
            link.attr('href','getReport/?json=' + JSON.stringify(datas[i]))
            nextsDiv.append(link)
            nextsDiv.append('<br>')
        }
    }
    var span = $(document.createElement('span'))
    span.text(name)
    this.div.append(span)

    this.div.append(this.sortDivsByIdDesc(nextsDiv))

}

PresentationNode.prototype.sortDivsByIdDesc = function(nextsDiv){
    if (nextsDiv.children('div').length > 1){
        changed = true
        while(changed){
            changed = false
            var newNextsDiv = $(document.createElement('div'))
            newNextsDiv.attr('style', nextsDiv.attr('style'))
            nextsDiv.children('div').each(function(){
                if (newNextsDiv.children('div').length > 0){
                    if (parseInt($(this).attr('id')) > parseInt(newNextsDiv.children('div').last().attr('id'))){
                        newNextsDiv.prepend($(this))
                        changed = true
                    } else {
                        newNextsDiv.append($(this))
                    }
                } else {
                    newNextsDiv.append($(this))
                }
            })
            nextsDiv = newNextsDiv
        }
        
    }
    return nextsDiv
}

PresentationNode.prototype.expand = function(url, datas){
    this.div.children('div').eq(0).show()
    this.div.children('button').eq(0).mousedown(this.close.bind(this))
    this.div.children('button').eq(0).text('-')
}

PresentationNode.prototype.close = function(url, datas){
    this.div.children('div').eq(0).hide()
    this.div.children('button').eq(0).mousedown(this.expand.bind(this))
    this.div.children('button').eq(0).text('+')
}

PresentationNode.prototype.createNextNodes = function(url, datas){
    var index = url.split('/')[0]
    var nextUrl = url.substring(url.indexOf('/')+1) //An easy way to split only on the first time
    var nextDatas = new Array()
    for (var i in datas){
        if (!(datas[i][index]['id'] in nextDatas)){
            nextDatas[ datas[i][index]['id'] ] = new Array()
        }
        nextDatas[ datas[i][index]['id'] ].push(datas[i])
    }
    this.nexts = new Array()
    for (var i in nextDatas){
        this.nexts.push(new PresentationNode( nextUrl, nextDatas[i], i, nextDatas[i][0][index]['name'] ))
    }
}

