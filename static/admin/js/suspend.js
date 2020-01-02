function initSuspendHtml(){
    var htmlstyle = '<style type="text/css" media="screen">'+
        'a { text-decoration:none; }'+
        '    a:hover { color:#2B4A78;text-decoration:underline; }'+
        '    a:focus, input:focus {outline-style:none; outline-width:medium; }'+
        '.pageNum{border: 1px solid #999;padding:2px 8px;display: inline-block;}'+
        '.cPageNum{font-weight: bold;padding:2px 5px;}'+
        '#pageNav a:hover{text-decoration:none;background: #fff4d8; }'+

        '</style>';
    $("head").append(htmlstyle)
	var html = 	
	'<section id="left_section"></section>'+
	'<section id="center_section">'+
		'<table id="mytable">'+
			'<div id="alt-msg">正在加载数据。。。</div>'+
		'</table>'+
        '<div id="pageNav"></div>'+
	'</section>';
	$("#content").html(html);
	$("h1").text("SUSPEND");
    initSuspendPageTool();
}

function initSuspendPageTool(){
    pageNav.pre="PRE";
    pageNav.next="NEXT";
    pageNav.fn = function(p,pn){
        //document.getElementById("test").innerHTML ="Page:"+p+" of "+pn + " pages.";
        //$("#test").text("Page:"+p+" of "+pn + " pages."); //for jquery
        var dataUrl = "/suspend?num=30&skipNum="+(parseInt(p)-1)*30;
        getDataAjax(dataUrl,processDataSuspend,"GET");
    };
    $.ajax({
        type: "GET",
        url: "/suspend_count",
        statusCode: {
            403: function() {
                location.href="/login.html";
            },
            500: function() {
                location.href="/login.html";
            },
            502: function() {
                location.href="/login.html";
            }
        },
        success: function(data){
            pageNav.go(1,Math.ceil(data[0]['count']/30));
        }
    });    
}

function processDataSuspend(data){
    var html = "<thead><tr>"
            + "<th style='width:20%;'>name</th>"
            + "<th style='width:20%;'>ip</th>"
            + "<th style='width:20%;'>created_time</th>"
            + "<th style='width:20%;'>status</th>";
            html +=  "<th style='width:20%;'>id</th>";
            html += "</tr></thead><tbody>";
    $.each(
            data[0]['result'],
            function(index, entry) {
                var dt = new Date();
                html += "<tr>"
                        + "<td >" + entry['name'] + "</td>"
                        + "<td >" + entry['ip'] + "</td>"
                        + "<td >"
                        + $.format.date( new Date( parseInt(entry['created_time']['$date']) + (dt.getTimezoneOffset() * 60000)), 'yyyy-MM-dd HH:mm:ss') + "</td>"
                        + "<td >"+entry['status']+"</td>";
                        html+= "<td >"+entry['id']+"</td>"
                        html += "</tr>";
            });
    html += "</tbody>";
    $("#alt-msg").html("");
    $("#mytable").html(html);
    $("#mytable").tablesorter();
    
}