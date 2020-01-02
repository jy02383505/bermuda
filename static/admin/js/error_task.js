function initErrorTaskHtml(){
	var html = 	
	'<section id="left_section"></section>'+
	'<section id="center_section">'+
		'<table id="mytable">'+
			'<div id="alt-msg">正在加载数据。。。</div>'+
		'</table>'+
		'<div id="show" style="display: none;"></div>'+
	'</section>';
	$("#content").html(html);
	$("h1").text("失败任务");
	var dataUrl = "/error_task";
    getDataAjax(dataUrl,processDataErrorTask,"GET");
}

function processDataErrorTask(data){
    var right = $("#userInfo").attr("name");
    var html = "<thead><tr>"
            + "<th style='width:10%;'>host</th>"
            + "<th style='width:15%;'>devName</th>"
            + "<th style='width:18%;'>created_time</th>"
            + "<th style='width:50%;'>url</th>";
            if(right=="admin" || right == "operator"){
                html +=  "<th style='width:7%;'>retry</th>";
            }
            html += "</tr></thead><tbody>";
    var divstr = "";
    $.each(
            data,
            function(index, entry) {
                var dt = new Date();
                var urlstr = "";
                $.each(entry['urls'], function(index, data) {
                    urlstr += data['url'];
                });
                var urls = urlstr.length <= 80 ? urlstr : urlstr.substring(0, 80) + "...";
                html += "<tr>"
                        + "<td >" + entry['host'] + "</td>"
                        + "<td >" + "<a class='retry_dev' href='#' title='点击重刷"+entry['devName']+"上最近20个失败的任务'>" + entry['devName'] + "</a>" + "</td>"
                        + "<td >"
                        + $.format.date( new Date( parseInt(entry['created_time']['$date']) + (dt.getTimezoneOffset() * 60000)), 'yyyy-MM-dd HH:mm:ss') + "</td>"
                        + "<td ><a class='detail'id='url"+index+"' href='#url_content"+index+"'>" + urls + "</a></td>";
                        if(right=="admin" || right == "operator"){
                            html+= "<td ><a class='retry' id='"+entry['_id']['$oid']+"' href='#'>retry</a></td>"
                        }
                        html += "</tr>";
                divstr += "<div class='divcontent' id='url_content"+index+"' style='width:800px;height:400px;overflow:auto;'>";
                $.each(entry["urls"], function(
                        index, data) {
                    divstr += data['url']
                            + "<br/>";
                });
                divstr += "</div>";
            });
    html += "</tbody>";
    $("#alt-msg").html("");
    $("#mytable").html(html);
    $("#mytable").tablesorter();
    $("#show").html(divstr);
    $("a.detail").fancybox({
        'titlePosition' : 'inside',
        'transitionIn' : 'none',
        'transitionOut' : 'none'
    })
    $("a.detail").parent().click(function() {
        $(this).find("a").click();
    });
    $("a.retry").click(
            function() {
                var curThis = this;
                var errorTaskId = $(this).attr('id');
                startWait();
                $.post("/retry_error_task/"
                        + errorTaskId, function(data) {
                    alert(data);
                    if (data != "failed") {
                        initErrorTaskHtml();
                    }else{
                        stopWait();
                    }
                })
            });
    $("a.retry_dev").click(
            function() {
                var curThis = this;
                var dev_name = $(this).text();
                var r = confirm("确认重试" + dev_name
                        + "上最近20条失败任务吗？")
                if (r == true) {
                    startWait();
                    $.post("/retry_error_device/"
                            + dev_name, function(data) {
                        alert(data);
                        initErrorTaskHtml();
                    })
                }
            }
    );
}