function initTimeOutsHtml(){
	var html = '<section id="left_section"></section>'+
				'<section id="center_section">'+
				'	<table id="mytable">'+
				'	<div id="alt-msg">正在加载数据。。。</div>'+
				'	</table>'+
				'	<div id="show" style="display: none;"></div>'+
				'</section>';
	$("#content").html(html);
    $("h1").text("超时链接");
	var dataUrl = "/url/timeouts";
	getDataAjax(dataUrl,processDataTimeOuts,"GET");

}

function processDataTimeOuts(data){
    var html = "<thead><tr>"
            + "<th style='width:8%;'>username</th>"
            + "<th style='width:6%;'>channel_code</th>"
            + "<th style='width:6%;'>status</th>"
            + "<th style='width:8%;'>isdir</th>"
            + "<th style='width:8%;'>action</th>"
            + "<th style='width:18%;'>created_time</th>"
            + "<th style='width:8%;'>is_multilayer</th>"
            + "<th style='width:30%;'>url</th>"
            + "<th style='width:8%;'>ID</th>"
            + "</tr></thead><tbody>";
    var divstr = "";
    $.each(data['dirs'],function(index, entry) {
                        var dt = new Date();
                        var urls =  entry['url'].length <= 80 ? entry['url']: entry['url'].substring(0,80)+ "...";
                        html += "<tr>"
                                + "<td >" + entry['username'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['channel_code'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['status'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['isdir'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['action'] + "</td>"
                                + "<td style='text-align:center;'>" + $.format.date( new Date( parseInt(entry['created_time']['$date']) + (dt.getTimezoneOffset() * 60000)), 'yyyy-MM-dd HH:mm:ss') + "</td>"
                                + "<td style='text-align:center;'>" + entry['is_multilayer'] + "</td>"
                                + "<td >" + urls + "</td>"
                                + "<td style='text-align:left;'>" + entry['_id']['$oid'] + "</td>"
                                + "</tr>";
                    });
    $.each(data['urls'],function(index, entry) {
                        var dt = new Date();
                        var urls =  entry['url'].length <= 80 ? entry['url']: entry['url'].substring(0,80)+ "...";
                        html += "<tr>"
                                + "<td >" + entry['username'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['channel_code'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['status'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['isdir'] + "</td>"
                                + "<td style='text-align:center;'>" + entry['action'] + "</td>"
                                + "<td style='text-align:center;'>" + $.format.date( new Date( parseInt(entry['created_time']['$date']) + (dt.getTimezoneOffset() * 60000)), 'yyyy-MM-dd HH:mm:ss') + "</td>"
                                + "<td style='text-align:center;'>" + entry['is_multilayer'] + "</td>"
                                + "<td >" + urls + "</td>"
                                + "<td style='text-align:left;'>" + entry['_id']['$oid'] + "</td>"
                                + "</tr>";
                    });
    html += "</tbody>";
    $("#alt-msg").html("");
    $("#mytable").html(html);
    if(data.length>0){
        $("#mytable").tablesorter();
    }
};