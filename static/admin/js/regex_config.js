function initRegexConfigHtml(){
    var right = $("#userInfo").attr("name");
    var html = '<section id="right">';
    if(right=="admin" || right == "operator"){
        html += 
    '<div class="top-div">'+
        '<div class="search-box">'+
            '<div class="search">'+
            '    username:&nbsp;<input id="username" class="text" type="text" value="" style="width: 150px;" >'+
            '</div>'+
            '<div class="search">'+
            '    type:&nbsp;'+
            '       <select id="isdir">'+
            '         <option value ="URL">URL</option>'+
            '         <option value ="DIR">DIR</option>'+
            '       </select>'+
            '</div>'+
            '<div class="search">'+
            '    regex:&nbsp;<input type="text" id="regex" class="text" value="" style="width: 200px;"/>'+
            '</div>'+
            '<div class="search">'+
            '    append:&nbsp;<input type="text" id="append" class="text" value="" style="width: 200px;"/>'+
            '</div>'+
            '<div class="search">'+
            '    ignore:&nbsp;<input type="text" id="ignore" class="text" value="" style="width: 200px;"/>'+
            '</div>'+
            '<div class="search submit">'+
            '    <input type="button" value="新增正则配置" id="submit"/>'+
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
    $("h1").text("正则配置");
    $('div.search input.text').addClass('search_font_style');
    var dataUrl = "/regexconfiglist";
    getDataAjax(dataUrl,processDataRegexConfig,"GET");
    
    $('#submit').click(function() {
    var username = $('#username').val().trim();
    var isdir = $('#isdir').val().trim();
    var regex = $('#regex').val().trim();
    var append = $('#append').val().trim();
    var ignore = $('#ignore').val().trim();
    if (ignore == ""){
        ignore = "no ignore";
    }
    if (username == "" || regex=="" ) {
        alert("输入信息不能为空!");
        return;
    }
    $.get(
        "/add_regexconfig",
        {"username":username,"isdir":isdir,"regex":regex,"append":append,"ignore":ignore},
        function(data){
            alert(data);
            var dataUrl = "/regexconfiglist";
            getDataAjax(dataUrl,processDataRegexConfig,"GET");
        }
        );
    
});
}

function processDataRegexConfig(data){
    try{
        var right = $("#userInfo").attr("name");
        var table = "<table id='mytable'><thead>"
                +"<tr>"
                +"<th style='width:15%;'>USERNAME</th>"
                +"<th style='width:15%;'>ISDIR</th>"
                +"<th style='width:20%;'>REGEX</th>"
                +"<th style='width:15%;'>APPEND</th>"
                +"<th style='width:15%;'>IGNORE</th>";
        if(right=="admin" || right == "operator"){
            table+="<th style='width:10%;'>操作</th>"
                +"</tr>";
        }
            table+="</thead><tbody";
        $.each(data, function(index, entry) {
            table += "<tr>";
            table += "<td>"+entry["username"]+"</td>";
            table += "<td>"+entry["isdir"]+"</td>";
            table += "<td>"+entry["regex"]+"</td>";
            table += "<td>"+entry["append"]+"</td>";
            table += "<td>"+entry["ignore"]+"</td>";
            if(right=="admin" || right == "operator"){
                table += "<td><a class='del' id='"+entry["id"]+"'>删除</a></td>";
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
        bindDelRegexConfig();
    }catch(err){
            alert(err)
            stopWait();
    }
}

function bindDelRegexConfig(){
    $('a.del').click(function(){
    if(confirm("确定删除此正则配置？")){
        var regexConfigId = $(this).attr('id');
        var username = $(this).parent().prev().prev().prev().prev().prev().html();
        $.get("/del_regexconfig",
            {"regexConfigId":regexConfigId,"username":username},
            function(data){
                alert(data);
                initRegexConfigHtml()
            });
        }
    });
}