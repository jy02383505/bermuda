function initChannelignoreHtml(){
    var right = $("#userInfo").attr("name");
	var html = '<section id="right">';
    if(right=="admin" || right == "operator"){
        html +=
    '<div class="top-div">'+
    '    <div class="search-box">'+
    '        <div class="search">'+
    '            CHANNEL_NAME:<input id="channel_name" class="text" type="text" value=""style="width: 350px;" >'+
    '        </div>'+
    '        <div class="search submit">'+
    '            <input type="button" value="新增" id="submit"/>'+
    '        </div>'+
    '    </div>'+
    '    <div class="clear"></div>'+
    '</div>';
    }
    html +=
    '<div class="middle-div">'+
    '</div>'+
    '<div class="clear"></div>'+
    '<div id="show" style="display: none">'+
    '    <div id="show-content" style="width: 768px;height:1024px;height:auto;min-height:1024px;"></div>'+
    '</div>'+
    '</section>';
    
    $("#content").html(html);
	$("h1").text("忽略大小写频道");
	$('div.search input.text').addClass('search_font_style');
    var dataUrl = "/channelignorelist";
    getDataAjax(dataUrl,processDataChannelignore,"GET");
    $('#submit').click(function() {
        var channel_name = $('#channel_name').val().trim();
        if (channel_name == "" ) {
            return;
        }
        try{
            startWait();
            $.ajax({
                type:"GET",
                url:"/add_channel",
                data:{"CHANNEL_NAME":channel_name},
                 statusCode: {
                    401: function() {
                        stopWait();
                        alert("no right");
                    },
                    504: function() {
                        stopWait();
                        alert("connection time out");
                    }
                },
                success: function(data){
                    alert(data);
                    var dataUrl = "/channelignorelist";
                    getDataAjax(dataUrl,processDataChannelignore,"GET");
                }
            });
        }catch(err){
            alert(err);
            stopWait();
        }
    
	});
	
}


function processDataChannelignore(data){
    try{
        var right = $("#userInfo").attr("name");
        var table = "<table id='mytable'><thead>"
                +"<tr>"
                +"<th style='width:45%;'>CHANNEL_NAME</th>"
                +"<th style='width:45%;'>CHANNEL_CODE</th>";
            if(right=="admin" || right == "operator"){
                table+="<th style='width:10%;'>操作</th>";
            }
                table+="</tr>"
                +"</thead><tbody";
        $.each(data, function(index, entry) {
            table += "<tr>";
            table += "<td>"+entry["CHANNEL_NAME"]+"</td>";
            table += "<td>"+entry["CHANNEL_CODE"]+"</td>";
            if(right=="admin" || right == "operator"){
                table += "<td><a class='del' id='"+entry["CHANNEL_NAME"]+"'>删除</a></td>";
            }
            table += "</tr>"
        });
        table += "</tbody></table>";
        $('div.middle-div').html(table);
        if(data.length>0){
            if (checkBrowser()){
                $("#mytable").tablesorter();
            }
        }
        bindDelChannelIgnore();
    }catch(err){
        alert(err)
        stopWait();
    }
}

function bindDelChannelIgnore(){
    $('a.del').click(function(){
        if(confirm("确定删除此忽略大小写？")){
            var channel_name = $(this).attr('id');
            $.ajax({
                type:"GET",
                url:"/del_channel",
                data:{"CHANNEL_NAME":channel_name},
                 statusCode: {
                    401: function() {
                        alert("no right");
                    }
                },
                success: function(data){
                    alert(data);
                    var dataUrl = "/channelignorelist";
                    getDataAjax(dataUrl,processDataChannelignore,"GET");
                }
            });
    	}
    });
}