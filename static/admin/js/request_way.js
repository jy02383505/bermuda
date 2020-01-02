
function initRequestWayHtml(){
 var html= '<div class="top-div">'+
        '<div class="search-box" style="padding-left: 10%；">'+
            '<div class="search" style="padding-left:15px;">'+
                '<label>requestID : &nbsp;</label>'+
                '<input id="requestID" class="text" style="width: 500px;" type="text" value="" >'+
            '</div>'+
            '<div class="search submit">'+
                '<input type="image" src="/btn_submit.png" id="request_submit"/>'+
            '</div>'+
        '</div>'+
        '<div class="clear"></div>'+
    '</div>'+
    '<div class="middle-div">'+
        '<div><span style="color:red;"><h2>Request:</h2></span></div>'+
        '<table id="mytable">'+
        '</table>'+
        '<div><span style="color:red;"><h2>callback:</h2></span><span id="callback_addr" ></span></div>'+
        '<br/>'+
        '<div><span style="color:red;"><h2>URL and DIR:</h2></span></div>'+
        '<table id="url_table">'+
        '</table>'+
    '</div>'+
    '<div id="page" style="padding-left:20px;">'+
    '</div>'+
    '<div class="clear"></div>'+
    '<div id="show" style="display: none">'+
        '<div id="show-content" style="width: 768px;height:1024px;height:auto;min-height:1024px;"></div>'+
    '</div>';
    $("#content").html(html);
    $("h1").text("request详情");
    $('div.search input.text').addClass('search_font_style');
    $('#request_submit').click(function() {
        var requestID = $('#requestID').val().trim();
        if(requestID != ""){
            var dataUrl = "/url/" + requestID ;
            getDataAjax(dataUrl+"/request",processDataRequestWay,"GET");
            getDataAjax(dataUrl,processDataRequestWayDetail,"GET");
        }else{
            alert("requestID 为空!");
        }
    });
}
function processDataRequestWay(data) {
        var table = "<thead>"
                +"<tr>"
                +"<th style='width: 10%;'>requestID</div>"
                +"<th style='width: 10%'>username</div>"
                +"<th style='width: 10%'>状态</div>"
                +"<th style='width: 20%'>创建时间</div>"
                +"<th style='width: 20%'>结束时间</div>"
                +"<th style='width: 10%'>耗时</div>"
                +"<th style='width: 10%;'>unprocess</div>"
                +"<th style='width: 10%'>remote_addr</div>"
                +"</tr>"
                +"</thead><tbody>";
            var dt = new Date();
            table += "<tr id='tr"+index+"'>";
            table += "<td>"+data['_id']['$oid']+"</div>";
            table += "<td>"+data["username"]+"</div>";
            table += "<td>"+data["status"]+"</div>";
            table += "<td>"+$.format.date(new Date(parseInt(data['created_time']['$date'])+(dt.getTimezoneOffset()*60000)),'yyyy-MM-dd HH:mm:ss')+"</div>";
            table += "<td>"+(data["finish_time"]==null?data["finish_time"]:$.format.date(new Date(parseInt(data['finish_time']['$date'])+(dt.getTimezoneOffset()*60000)),'yyyy-MM-dd HH:mm:ss'))+"</div>";
            table += "<td>"+(data["finish_time"]==null? 0  : (parseInt(data['finish_time']['$date'])-parseInt(data['created_time']['$date']))/1000)+"(s)</div>";
            table += "<td>"+data["unprocess"]+"</div>";
            table += "<td>"+data["remote_addr"]+"</div>";
            table += "</tr>";
        table += "</tbody>";
        $('#mytable').html(table);
        if (data['callback'] !=null){
            var callback_url = data['callback']['url'] == null?"no callback_url":data['callback']['url'];
            var callback_email = data['callback']['email'] == null?"no callback_email": data['callback']['email'];
        }else{
            var callback_url = "no callback_url";
            var callback_email = "no callback_email";
        }
        $('#callback_addr').html("<p>"+callback_url+"</p>"+"<p>"+callback_email+"</p>");
    }

function processDataRequestWayDetail(data) {
        var table = "<thead>"
                +"<tr>"
                +"<th style='width: 6%;'>id</div>"
                +"<th style='width: 6%'>dev_id</div>"
                +"<th style='width: 4%'>isdir</div>"
                +"<th style='width: 6%'>ignore</div>"
                +"<th style='width: 6%;'>mulil</div>"
                +"<th style='width: 6%'>状态</div>"
                +"<th style='width: 20%'>创建时间</div>"
                +"<th style='width: 20%'>结束时间</div>"
                +"<th style='width: 10%'>耗时</div>"
                +"<th style='width: 16%;'>url</div>"
                +"</tr>"
                +"</thead><tbody>";
            $.each(data['results'], function(index, entry) {
                var dt = new Date();
                table += "<tr id='tr"+index+"'>";
                table += "<td><a id='"+(entry['dev_id']==null?"noid":entry['dev_id']['$oid'])+"'class='popup' style='padding-left:10px;text-decoration:none;' href='#show-content' title='点击查看设备结果'>"+entry['_id']['$oid']+"</a></div>";
                table += "<td><a id='"+(entry['dev_id']==null?"noid":entry['dev_id']['$oid'])+"'class='popup' style='padding-left:10px;text-decoration:none;' href='#show-content' title='点击查看设备结果'>"+(entry['dev_id']==null?"noid":entry['dev_id']['$oid'])+"</a></div>";
                table += "<td>"+entry["isdir"]+"</div>";
                table += "<td>"+entry["ignore_case"]+"</div>";
                table += "<td>"+entry["is_multilayer"]+"</div>";
                table += "<td>"+entry["status"]+"</div>";
                table += "<td>"+$.format.date(new Date(parseInt(entry['created_time']['$date'])+(dt.getTimezoneOffset()*60000)),'yyyy-MM-dd HH:mm:ss')+"</div>";
                table += "<td>"+(entry["finish_time"]==null?entry["finish_time"]:$.format.date(new Date(parseInt(entry['finish_time']['$date'])+(dt.getTimezoneOffset()*60000)),'yyyy-MM-dd HH:mm:ss'))+"</div>";
                table += "<td>"+(entry["finish_time"]==null? 0  : (parseInt(entry['finish_time']['$date'])-parseInt(entry['created_time']['$date']))/1000)+"(s)</div>";
                table += "<td><a id='"+(entry['dev_id']==null?"noid":entry['dev_id']['$oid'])+"'class='popup' style='padding-left:10px;text-decoration:none;' href='#show-content' title='点击查看设备结果'>"+(entry['url']==null?"nourl":entry['url'])+"</a></div>";
                table += "</tr>";
            });
        table += "</tbody>";
        $('#url_table').html(table);
        bindPopUpDetail();
    }
