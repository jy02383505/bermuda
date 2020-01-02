function initRewriteHtml(){
    var right = $("#userInfo").attr("name");
	var html = '<section id="right">';
    if(right=="admin" || right == "operator"){
        html += 
    '<div class="top-div">'+
        '<div class="search-box">'+
            '<div class="search">'+
            '    CHANNEL:<input id="channel_name" class="text" type="text" value=""style="width: 350px;" >'+
            '</div>'+
            '<div class="search">'+
            '    REWRITE:<input type="text" id="rewrite_name" class="text" value="" style="width: 350px;"/>'+
            '</div>'+

            '<div class="search submit">'+
            '    <input type="button" value="新增" id="submit"/>'+
            '</div>'+
        '</div>'+
        '<div class="clear"></div>'+
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
	$("h1").text("REWRITE");
	$('div.search input.text').addClass('search_font_style');
    var dataUrl = "/rewritelist";
    getDataAjax(dataUrl,processDataRewrite,"GET");
    
    $('#submit').click(function() {
    var channel_name = $('#channel_name').val().trim();
    var rewrite_name = $('#rewrite_name').val().trim();
    if (channel_name == "" || rewrite_name=="" ) {
        return;
    }
    $.get(
    	"/add_rewrite",
    	{"CHANNEL_NAME":channel_name,"REWRITE_NAME":rewrite_name},
    	function(data){
    		alert(data);
    		var dataUrl = "/rewritelist";
    		getDataAjax(dataUrl,processDataRewrite,"GET");
    	}
    	);
    
});
}

function processDataRewrite(data){
    try{
        var right = $("#userInfo").attr("name");
        var table = "<table id='mytable'><thead>"
                +"<tr>"
                +"<th style='width:45%;'>CHANNEL_NAME</th>"
                +"<th style='width:45%;'>REWRITE_NAME</th>";
        if(right=="admin" || right == "operator"){
            table+="<th style='width:10%;'>操作</th>"
                +"</tr>";
        }
            table+="</thead><tbody";
        $.each(data, function(index, entry) {
            $.each(entry["REWRITE_NAME"],function(key_rewrite,value_rewrite){
                table += "<tr>";
                table += "<td>"+entry["CHANNEL_NAME"]+"</td>";
                table += "<td>"+value_rewrite+"</td>";
                if(right=="admin" || right == "operator"){
                    table += "<td><a class='del' id='"+entry["CHANNEL_NAME"]+"'>删除</a></td>";
                }
                table += "</tr>"     
            })
        });
        table += "</tbody></table>";
        $('div.middle-div').html(table);
        if(data.length>0){
            if (checkBrowser()){
                $("#mytable").tablesorter();
            }
        }
        bindDelRewrite();
    }catch(err){
            alert(err)
            stopWait();
    }
}

function bindDelRewrite(){
    $('a.del').click(function(){
    if(confirm("确定删除此重定向？")){
        var channel_name = $(this).attr('id');
        var rewrite_name = $(this).parent().prev().text();
        $.get("/del_rewrite",
        	{"CHANNEL_NAME":channel_name,"REWRITE_NAME":rewrite_name},
            function(data){
                alert(data);
                initRewriteHtml()
                //var dataUrl = "/rewritelist";
				//getDataAjax(dataUrl,processDataRewrite,"GET");
            });
    	}
	}
    );
}