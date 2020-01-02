function initClearBlackListHtml(){
	var html = '<section id="left_section">'+
        '</section>'+
        '<section id="center_section">';
    var right = $("#userInfo").attr("name");
    if(right=="admin" || right == "operator"){
        html += '<input type="button" value="清除全部黑名单" id="clear_all"/>'
    }
        html +='<table id="mytable" >'+

            '</table>'+
            '<div id="show" style="display: none;">'+
            '</div>'+
        '</section>';
	$("#content").html(html);
    $("h1").text("黑名单");
	var dataUrl = "/blacklist";
    getDataAjax(dataUrl,processDataClearBlackList,"GET");
    $("#clear_all").click(function(){
	    $.getJSON(
	            "/clear_blacklist",
	            function(data){
	                $.each(data,function(index,entry){
	                    alert(entry['result']);
	                })
	                location.reload();
	            }
	    );
	});
}

function processDataClearBlackList(data){
    var right = $("#userInfo").attr("name");
    var tableHtml = "<thead><tr>"+
            "<th style='width:30%;'>host</th>"+
            "<th style='width:60%;'>error_str</th>";
            if(right=="admin" || right == "operator"){
                tableHtml += "<th style='width:10%;'>operation</th>";
            }
            tableHtml += "</tr></thead><tbody>";
    $.each(data,function(index,entry){
        tableHtml += "<tr>"+
                "<td >"+entry['host']+"</td>"+
                "<td >"+entry['error_str']+"</td>";
                if(right=="admin" || right == "operator"){
                   tableHtml += "<td ><a class='detail'id='url"+index+"' href='#/"+index+"'>"+"</a></td>";
                }
                tableHtml+"</tr>";
    });
    tableHtml +="</tbody>";
    $("#mytable").html(tableHtml);
}
