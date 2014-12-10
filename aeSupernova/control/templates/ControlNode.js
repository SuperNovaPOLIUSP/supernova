function ControlNode(url, datas, id, name){
    this.id = id
    this.name = name
    this.div = $(document.createElement('div')) 
    this.div.attr('id',id)
    this.nexts = null

    var nextsDiv = $(document.createElement('div'))
    nextsDiv.attr('style', 'position:relative; left:35px; display: block;')
    nextsDiv.show()

    this.numberOfAnswers = 0
    if (url != ''){
        this.createNextNodes(url, datas)

        var button = $(document.createElement('button'))
        button.text('-')
        button.mousedown(this.close.bind(this))
        this.div.append(button)
        var nextHaveNext = false
        for (var i in this.nexts){
            if (this.nexts[i].nexts != null){
                nextHaveNext = true
            }
            nextsDiv.append(this.nexts[i].div)
            this.numberOfAnswers = this.numberOfAnswers + this.nexts[i].numberOfAnswers
        }
    } else {
        nextHaveNext = false
        this.datas = datas
        for (var i in datas){
            this.numberOfAnswers = this.numberOfAnswers + parseInt(datas[i]['datafile']['numberOfAnswers'])
        }
    }

    var span = $(document.createElement('span'))
    span.text('		' + name + '   - ' + this.numberOfAnswers)
    this.div.append(span)

    this.div.append(nextsDiv)
    if (!nextHaveNext){
        this.close()
    }

}

ControlNode.prototype.expand = function(url, datas){
    this.div.children('div').eq(0).show()
    this.div.children('button').eq(0).mousedown(this.close.bind(this))
    this.div.children('button').eq(0).text('-')
}

ControlNode.prototype.close = function(url, datas){
    this.div.children('div').eq(0).hide()
    this.div.children('button').eq(0).mousedown(this.expand.bind(this))
    this.div.children('button').eq(0).text('+')
}

ControlNode.prototype.createNextNodes = function(url, datas){
    var index = url.split('/')[0]
    var nextUrl = url.split(index + '/')[1]
    var nextDatas = new Array()
    for (var i in datas){
        if (!(datas[i][index]['id'] in nextDatas)){
            nextDatas[ datas[i][index]['id'] ] = new Array()
        }
        nextDatas[ datas[i][index]['id'] ].push(datas[i])
    }
    this.nexts = new Array()
    for (var i in nextDatas){
        this.nexts.push(new ControlNode( nextUrl, nextDatas[i], i, nextDatas[i][0][index]['name'] ))
    }
}
