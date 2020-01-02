function initOverloadsHtml(){
    var right = $("#userInfo").attr("name");
	var html = '<section id="left_section"></section>'+
	'<section id="center_section">'+
        '<div class="top-div">';
    if(right=="admin" || right == "operator"){
        html +=
            '<div class="search-box">'+
                '<div class="search">'+
                 '   USERNAME&nbsp;:&nbsp;<input id="username" class="text" type="text" value=""style="width: 350px;" >'+
                '</div>'+
                '<div class="search">'+
                '    MAX_URL&nbsp;:&nbsp;<input type="text" id="max_url_num" class="text" value="0" style="width: 150px;"/>'+
                '</div>'+
                '<div class="search">'+
                '    MAX_DIR&nbsp;:&nbsp;<input type="text" id="max_dir_num" class="text" value="0" style="width: 150px;"/>'+
                '</div>'+
                '<div class="search submit">'+
                '    <input type="button" value="新增" id="submit"/>'+
                '</div>'+
            '</div>'+
            '<div class="clear"></div>'+
        '</div>'+
        '<hr/>';
    }
        html += 
        '<span style="padding-left: 45%;font-weight: bolder;color: #556b2f;">超量配置信息</span>'+
        '<table id="overloads-config-table">'+

        '</table>'+
        '<hr/>'+
        '<span  style="padding-left: 45%;font-weight: bolder;color: #556b2f;">当前超量信息<br/></span>'+
		'<table id="mytable">'+
		'	<div id="alt-msg">正在加载数据。。。</div>'+
		'</table>'+
		'<div id="show" style="display: none;"></div>'+
	'</section>';
	$("#content").html(html);
    $("h1").text(" 超量信息");
	var dataUrl = "/overloads";
    getDataAjax(dataUrl,processDataOverLoads,"GET");
    $('#submit').click(function() {
            var username = $('#username').val().trim();
            var max_url_num = $('#max_url_num').val().trim();
            var max_dir_num = $('#max_dir_num').val().trim();
            if (username == "" || max_url_num=="" || max_dir_num=="") {
                return;
            }
            $.get(
                    "/add_overloads_config",
                    {"USERNAME":username,"URL":max_url_num,"DIR":max_dir_num},
                    function(data){
                        alert(data);
                       	var dataUrl = "/overloads";
    					getDataAjax(dataUrl,processDataOverLoads,"GET");
                    }
            );

        });
}

function processDataOverLoads(data){
    var html = "<thead><tr>"
            + "<th style='width:60%;'>overload_key</th>"
            + "<th style='width:40%;'>value</th>"
            + "</tr></thead><tbody>";
    $.each(data,function(index, entry) {
        html += "<tr>"
                + "<td >"
                + entry['overload_key']
                + "</td>"
                + "<td >"
                + entry['value']
                + "</td>"
                + "</tr>";

    });
    html += "</tbody>";
    $("#alt-msg").html("");
    $("#mytable").html(html);
    if(data.length>0){
        $("#mytable").tablesorter();
    }
    var overLoadsConfigUrl = "/overloads_config_list";
    getDataAjax(overLoadsConfigUrl,processOverLoadsConfig,"GET");
}

function processOverLoadsConfig(data){
    var right = $("#userInfo").attr("name");
    var html = "<thead><tr>"
            + "<th style='width:20%;'>USERNAME</th>"
            + "<th style='width:30%;'>URL</th>"
            + "<th style='width:30%;'>DIR</th>";
        if(right=="admin" || right == "operator"){
            html += "<th style='width:20%;'>OPERATION</th>";
        }
            html+= "</tr></thead><tbody>";
    $.each(data,function(index, entry) {
        html += "<tr>"
                + "<td >"
                + entry['USERNAME']
                + "</td>"
                + "<td >"
                + entry['URL']
                + "</td>"
                + "<td >"
                + entry['DIR']
                + "</td>";
        if(right=="admin" || right == "operator"){
            html+= "<td >"
                + "<a class='del' id='"+entry["USERNAME"]+"'>删除</a>"
                + "</td>";
        }
            html+= "</tr>";

    });
    html += "</tbody>";
    $("#overloads-config-table").html(html);
    $("#overloads-config-table").tablesorter();
    bindDelOverloads();
}
function bindDelOverloads(){
    $('a.del').click(function(){
                if(confirm("确定删除此重定向？")){
                    var username = $(this).attr('id');
                    $.get("/del_overloads_config",
                            {"USERNAME":username},
                            function(data){
                                alert(data);
                                var dataUrl = "/overloads";
    							getDataAjax(dataUrl,processDataOverLoads,"GET");
                            });
                }
            }
    );
}