
function initRefreshDetailContent(){
 var html= '<div class="top-div">'+
        '<div class="search-box" style="padding-left: 10%；">'+
            '<div class="search" style="padding-left:15px;">'+
                '<label>用户名 : &nbsp;</label>'+
                '<input id="customer" class="text" type="text" value="用户名" >'+
            '</div>'+
            '<div class="search">'+
                '<input type="text" id="url" class="text" value="URL查询" style="width: 500px;"/>'+
            '</div>'+
            '<div class="search">'+
                '<select id="status">'+
				  '<option value ="ALL">ALL</option>'+
				  '<option value ="FINISHED">FINISHED</option>'+
				  '<option value="PROGRESS">PROGRESS</option>'+
				'</select>'+
            '</div>'+
            '<div class="search">'+
                '<label>日期 ： </label><input type="text" id="beginDate" class="datepicker"  readonly="true" name="beginDate"/>'+
            '</div>'+
            '<div class="search submit">'+
                '<input type="image" src="/btn_submit.png" id="submit"/>'+
            '</div>'+
        '</div>'+
        '<div class="clear"></div>'+
    '</div>'+
    '<div class="middle-div">'+
        '<table id="mytable">'+

        '</table>'+
    '</div>'+
    '<div id="page" style="padding-left:20px;">'+
    '</div>'+
    '<div class="clear"></div>'+
    '<div id="show" style="display: none">'+
        '<div id="show-content" style="width: 768px;height:1024px;height:auto;min-height:1024px;"></div>'+
    '</div>';
	$("#content").html(html);
	$("h1").text("刷新详情");
    $('.datepicker').datepicker();
    $('.datepicker').datepicker( 'setDate' , new Date());
    $('#ui-datepicker-div').css("display","None");
    $('div.search input.text').addClass('search_font_style');
    inintPageHtml(); // 
    var customerId = $('#customer').val().trim();
    var status = $('#status').val().trim();
    var url = "";
    var datestr = $(".datepicker").val();
    var num = $("#num").html().trim();
    var skipNum = 0;
    var dataUrl = "/user/"+customerId+"/urls?q="+url+"&date="+datestr+"&status="+status+"&num="+num+"&skipNum="+skipNum;
    $("#query").html(dataUrl)
    getDataAjax(dataUrl,processDataRefreshDetail,"GET");
    $('#submit').click(function() {
        var customerId = $('#customer').val().trim();
        var status = $('#status').val().trim();
        var url = $('#url').val().trim();
        var datestr = $(".datepicker").val();
        if (customerId == "" || customerId=="客户查询" ) {
            return;
        }
        if(url == "URL查询"){
            url = "";
        }
        var num = $("#num").html().trim();
        $("#curPage").html("1");
        var skipNum = 0;
        $('div.div-table').remove();
        var dataUrl = "/user/"+customerId+"/urls?q="+url+"&date="+datestr+"&status="+status+"&num="+num+"&skipNum="+skipNum;
        $("#query").html(dataUrl);
        getDataAjax(dataUrl,processDataRefreshDetail,"GET");
    });
}
function processDataRefreshDetail(data) {

        var table = "<thead>"
                +"<tr>"
                +"<th style='width: 32%;'>URL</div>"
                +"<th style='width: 10%'>是否是目录</div>"
                +"<th style='width: 8%'>状态</div>"
                +"<th style='width: 16%'>创建时间</div>"
                +"<th style='width: 16%'>结束时间</div>"
                +"<th style='width: 10%'>耗时</div>"
                +"<th style='width: 8%;'>ID</div>"
                +"</tr>"
                +"</thead><tbody>";
        $.each(data[0]['result'], function(index, entry) {
            var dt = new Date();
            table += "<tr id='tr"+index+"'>";
            table += "<td><a id='"+entry['dev_id']['$oid']+"'class='popup' style='padding-left:10px;text-decoration:none;' href='#show-content' title='点击查看设备结果'>"+entry["url"]+"</a></div>";//href='/url/"+entry["_id"]['$oid']+"/devices'
            table += "<td>"+entry["isdir"]+"</div>";
            table += "<td>"+entry["status"]+"</div>";
            table += "<td>"+$.format.date(new Date(parseInt(entry['created_time']['$date'])+(dt.getTimezoneOffset()*60000)),'yyyy-MM-dd HH:mm:ss')+"</div>";
            table += "<td>"+(entry["finish_time"]==null?entry["finish_time"]:$.format.date(new Date(parseInt(entry['finish_time']['$date'])+(dt.getTimezoneOffset()*60000)),'yyyy-MM-dd HH:mm:ss'))+"</div>";
            table += "<td>"+(entry["finish_time"]==null? 0  : (parseInt(entry['finish_time']['$date'])-parseInt(entry['created_time']['$date']))/1000)+"(s)</div>";
            table += "<td>"+entry["_id"]["$oid"]+"</div>";
            table += "</tr>";
        });
        table += "</tbody>";
        $('#mytable').html(table);
        bindPopUpDetail();
        var count = data[0]['count'];
        initPageTool(count);
        initPageItem();
    }

function inintPageHtml(){
    var pageHtml =  '<span id="config-page" style="display:none;"><span id="curPage">1</span><span id="num">25</span><span id="query"></span><span id="totalPage"></span></span>'+        
                    '<span id="prePage" style="cursor:pointer">上一页</span>'+
                    '<span id="pateItem">1 2 3</span>'+
                    '<span id="nextPage" style="cursor:pointer">下一页</span>'+
                    '<span id="pageDetail">(1-25/60)</span>'+
                    '<span>&nbsp;|&nbsp;每页显示:&nbsp;'+
                        '<a name="a_num" id="a_num_25" style="cursor:pointer;color:red;">25</a>,&nbsp;&nbsp;'+
                        '<a name="a_num" id="a_num_50" style="cursor:pointer;color:#2A5685;">50</a>,&nbsp;&nbsp;'+
                        '<a name="a_num" id="a_num_100" style="cursor:pointer;color:#2A5685;">100</a>'+
                    '</span>';
    $("#page").html(pageHtml);
    $("#config-page").hide();
    $("#prePage").hide();
    $("#nextPage").hide();
}
function initPageTool(count){
    var curPage = parseInt($("#curPage").html());
    var num = parseInt($("#num").html());
    var curMin = (num*(curPage-1)+1);
    var curMax = num*curPage;
    if(curMax>=count){
        curMax = count;
        $("#nextPage").hide();
    }else{
        $("#nextPage").show();
    }
    if(curPage>1){
        $("#prePage").show();
    }else{
        $("#prePage").hide();
    }
    if (count==0){
        curMax = 0;
        curMin = 0
    }
    $("#pageDetail").html("(" + curMin + "-" + curMax + "/" + count + ")");
    $("#totalPage").html(Math.ceil(count/num));
    $("#nextPage").unbind("click");
    $("#prePage").unbind("click");
    $("a[name=a_num]").unbind("click");
	$("#nextPage").click(function(){
        var curPage = parseInt($("#curPage").html())+1;
        var num = parseInt($("#num").html());
        $("#curPage").html(curPage);
        var dataUrlArr = $("#query").html().split("&amp;");
        dataUrlArr[4] = "skipNum="+num*(curPage-1);
        var dataUrl = dataUrlArr.join("&");
        getDataAjax(dataUrl,processDataRefreshDetail,"GET");
    });
    $("#prePage").click(function(){
        var curPage = parseInt($("#curPage").html())-1;
        var num = parseInt($("#num").html());
        $("#curPage").html(curPage);
        var dataUrlArr = $("#query").html().split("&amp;");
        dataUrlArr[4] = "skipNum="+num*(curPage-1);
        var dataUrl = dataUrlArr.join("&");
        getDataAjax(dataUrl,processDataRefreshDetail,"GET");
    });
    $("a[name=a_num]").click(function(){
        $("a[name=a_num]").css({"color":"#2A5685"});
        $(this).css({"color": "red"});
        var num = $(this).text();
        $("#num").html(num);
        var curPage = 1;
        $("#curPage").html(curPage);
        var dataUrlArr = $("#query").html().split("&amp;");
        dataUrlArr[3] = "num="+num;
        dataUrlArr[4] = "skipNum="+num*(curPage-1);
        var dataUrl = dataUrlArr.join("&");
        $("#query").html(dataUrl);
        getDataAjax(dataUrl,processDataRefreshDetail,"GET");   
    });
}


function initPageItem(){
    $("a[name='a_page']").unbind("click");
    var totalPage = parseInt($("#totalPage").html());
    var curPage = parseInt($("#curPage").html());
    var pageItemHtml = "";
    var limitShow = 1;
    var leftAndRight=2
        if (curPage>leftAndRight+limitShow){
            pageItemHtml += "<a name='a_page' style='cursor:pointer;color:#2A5685'>&nbsp;"+1+"&nbsp;</a>...";
        } 
        for(var i=curPage-leftAndRight;i+limitShow+leftAndRight-curPage<=totalPage&&i<=totalPage&&i<=(curPage+leftAndRight);i++){            
                var page = i;
                if(curPage-leftAndRight<=0){
                    page=i+(leftAndRight+limitShow-curPage);
                } 
                if(page==curPage){
                    pageItemHtml += "<a name='a_page' style='cursor:pointer;color:red;'>&nbsp;"+page+"&nbsp;</a>";
                }else{
                    pageItemHtml += "<a name='a_page' style='cursor:pointer;color:#2A5685'>&nbsp;"+page+"&nbsp;</a>";
                }
        }
        if (curPage+leftAndRight+limitShow<=totalPage ){
            pageItemHtml += "...<a name='a_page' style='cursor:pointer;color:#2A5685'>&nbsp;"+totalPage+"&nbsp;</a>";
        } 
    $("#pateItem").html(pageItemHtml);
    $("a[name='a_page']").click(function(){
        $("a[name=a_page]").css({"color":"#2A5685"});
        $(this).css({"color": "red"});
        var num = parseInt($("#num").html());
        var curPage = parseInt($(this).text());
        $("#curPage").html(curPage);
        var dataUrlArr = $("#query").html().split("&amp;");
        dataUrlArr[4] = "skipNum="+num*(curPage-1);
        var dataUrl = dataUrlArr.join("&");
        getDataAjax(dataUrl,processDataRefreshDetail,"GET");
    });
}

function bindPopUpDetail() {
    $('a.popup').click(function(){
        var rid = $(this).attr('id');
        $.getJSON("/url/"+rid+"/devices",
            function(data){
                var count = 0;
                var divContent =
                        "<div id='container' style='width: 768px;'>"+
                                "      <input type='hidden' name='urlId' id='urlId' value='"+rid+"'>"+
                                "       <div class='middle-div'>"+
                                "       <div id='summary' class='drop-shadow curved curved-vt-2'>"+
                                "       <div style='width: 50%;'>"+
                                "       <p class='title'>刷新设备数</p>"+
                                "      <p id='total_devices' class='value'>total_devices </p>"+
                                "       </div>"+
                                "       <div style='width: 50%;'>"+
                                "       <p class='title'>没有处理的设备数</p>"+
                                "      <p id='unprocess_devices' class='value'>unprocess_devices</p>"+
                                "       </div>"+
                                "       </div>"+
                                "       <div class='clear'></div>"+
                                "       <div class='div-table' id='table-devices'>"+
                                "       <div class='div-head'>"+
                                "       <div class='div-th' style='width: 30%; cursor: pointer;' id='hostname'>设备名字</div>"+
                                "       <div class='div-th' style='width: 15%; cursor: pointer;' id='status'>状态</div>"+
                                "       <div class='div-th' style='width: 10%; cursor: pointer;' id='code'>Code</div>"+
                                "       <div class='div-th' style='width: 30%'>IP</div>"+
                                "       <div class='div-th' style='width: 15%; cursor: pointer;' id='isfirstlayer'>是否上层</div>"+
                                "       <div class='clear'></div>"+
                                "       </div>";
                $.each(data['devices'],function(index,entry){
                    count = count+1;
                    divContent += "           <div class='div-tr level0' id='tr0'>"+
                                "               <div class='div-td' style='width: 30%'>"+entry['name'] +"</div>"+
                                "               <div class='div-td' style='width: 15%'>"+entry['status']  +"</div>"+
                                "                <div class='div-td' style='width: 10%'>"+entry['code']  +"</div>"+
                                "           <div class='div-td' style='width: 30%'>"+entry['host']  +"</div>"+
                                "           <div class='div-td' style='width: 15%'>"+entry['firstLayer']+" </div>"+
                                "           </div>";
                });
                divContent += "</div>"+
                            "</div>"+
                            "</div>";
                $("#show-content").html(divContent);
                $("#total_devices").html(count);
                $("#unprocess_devices").html(data['unprocess']);
            });
    });
    $('a.popup').fancybox({
        'width': "768",
        'height': "1024",
        'autoScale': true,
        'centerOnScroll': true,
        'padding': 28,
        'margin': 48,
        'scrolling': "no",
        'overlayOpacity': 0.4,
        'overlayColor': "#979b8f",
        'transitionIn': "elastic",
        'transitionOut': "elastic",
        'enableEscapeButton': true
    });
}
