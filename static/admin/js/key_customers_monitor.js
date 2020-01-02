function initKeyCustomersMonitorHtml(){
    var right = $("#userInfo").attr("name");
    var html = '<section id="right">';
      if(right=="admin"){
          html +=
      '<div class="top-div" style="min-height:120px;">'+
      '    <div class="search-box">'+
      '        <div class="search">'+
      '            USERNAME:<input id="username" class="text" type="text" value=""style="width: 256px;" >'+
      '            Monitor_Email:'+
      '        </div>'+
      '        <div class="search">'+
      '           <textarea id="monitor_email" name="monitor_email" style="width: 500px;resize: none;" rows="7"></textarea>'+
      '        </div>'+
      '        <div class="search submit">'+
      '            <input type="button" value="新增or修改" id="submit"/>'+
      '        </div>'+
      '    </div>'+
      '    <div class="clear"></div>'+
      '</div>';
      }
      html += 
      '<hr/> <div style="text-align:center;color:blue;">监控详情<div>' +
      '<div class="middle-div">'+
      '</div>'+
      '<div class="clear"></div>'+
      '<div id="show" style="display: none">'+
      '    <div id="show-content" style="width: 768px;height:1024px;height:auto;min-height:1024px;"></div>'+
      '</div>'+
      '</section>';
      
      $("#content").html(html);
    $("h1").text("重 点 客 户 监 控");
    $('div.search input.text').addClass('search_font_style');
    var dataUrl = "/key_customers_monitor_list";
    getDataAjax(dataUrl,processDataKeyCustomersMonitor,"GET");
    $('#submit').click(function() {
        var username = $('#username').val().trim();
        var monitor_email = $('#monitor_email').val().trim().split("\n").join(",");
        if (username == "" || monitor_email == "" ) {
            alert('用户名和接受邮件地址不能为空!');
            return;
        }
        try{
            startWait();
            $.ajax({
                type:"GET",
                url:"/add_key_customers_monitor",
                data:{"USERNAME":username,"Monitor_Email":monitor_email},
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
                    var dataUrl = "/key_customers_monitor_list";
                    getDataAjax(dataUrl,processDataKeyCustomersMonitor,"GET");
                }
            });
        }catch(err){
            alert(err);
            stopWait();
        }
    
  });
  
}


function processDataKeyCustomersMonitor(data){
    try{
        var right = $("#userInfo").attr("name");
        var dt = new Date();
        var table = "<table id='mytable'><thead>"
                +"<tr>"
                +"<th style='width:12%;text-align:center;'>客户名</th>"
                +"<th style='width:60%;text-align:center;'>Monitor_Email</th>"
                +"<th style='width:18%; text-align:center;'>最后监控时间</th>";
            if(right=="admin"){
                table+="<th style='width:10%;text-align:center;'>操作</th>";
            }
                table+="</tr>"
                +"</thead><tbody";
        $.each(data, function(index, entry) {
            table += "<tr>";
            table += "<td><a class='modify'>"+entry["USERNAME"]+"</a></td>";
            table += "<td>"+entry["Monitor_Email"]+"</td>";
            table += "<td>"+$.format.date( new Date( parseInt(entry['update_time']['$date']) + (dt.getTimezoneOffset() * 60000)), 'yyyy-MM-dd HH:mm:ss') + "</td>";
            if(right=="admin" ){
                table += "<td><a class='del' id='"+entry["USERNAME"]+"'>删除</a></td>";
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
        bindDelKeyCustomersMonitor();
        bindModifyKeyCustomersMonitor();
    }catch(err){
        alert(err)
        stopWait();
    }
}

function bindModifyKeyCustomersMonitor(){
    $('a.modify').unbind();
    $('a.modify').click(function(){
        $("#username").val($(this).text());
        var monitor_email = $(this).parent().next().text().split(',');
        var html = ""
        $.each(monitor_email,function(index,entry){
          html += entry + "\n";
        });
        $("#monitor_email").val(html)
    });
}

function bindDelKeyCustomersMonitor(){
    $('a.del').unbind();
    $('a.del').click(function(){
        if(confirm("确定删除此忽略大小写？")){
            var username = $(this).attr('id');
            $.ajax({
                type:"GET",
                url:"/del_key_customers_monitor",
                data:{"USERNAME":username},
                 statusCode: {
                    401: function() {
                        alert("no right");
                    }
                },
                success: function(data){
                    alert(data);
                    var dataUrl = "/key_customers_monitor_list";
                    getDataAjax(dataUrl,processDataKeyCustomersMonitor,"GET");
                }
            });
      }
    });
}