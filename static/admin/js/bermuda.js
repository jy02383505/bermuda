function checkBrowser(){
    if($.browser.safari || $.browser.mozilla || $.browser.opera){
        return true;
    }
    if($.browser.msie && parseInt($.browser['version'])>=9){
        return true;
    }
}

function getDataAjax(dataUrl,processData,typeStr){
    startWait();
    $.ajax({
        type: typeStr,
        url: dataUrl,
        statusCode: {
            403: function() {
                location.href="/login.html";
            },
            502: function() {
                location.href="/login.html";
            },
            500: function() {
                stopWait();
            },
            504: function() {
                stopWait();
            }
        },
        success: function(data){
            try{
                processData(data);
            }catch(err){
               alert(err);
               stopWait(); 
            }finally{
                stopWait();
            }

            }
        });
}

function initTopMenu(){
    var roles = $("#userInfo").attr("name");
    var html = '<ul id="nav">'+
                        '<li><a name="top-a" id="index">首页</a></li>'+
                        '<li><a name="top-a" id="refresh_detail">结果查询</a></li>'+
                        '<li><a name="top-a" id="second-menu" title="结果查询">信息查询</a>'+
                        '     <ul>'+
                        '         <li><a name="top-a" id="clear_blacklist">黑名单</a></li>'+
                        '         <li><a name="top-a" id="timeouts">超时查询</a></li>'+
                        '         <li><a name="top-a" id="error_task">失败任务</a></li>'+
                        '         <li><a name="top-a" id="rewrite">重定向查询</a></li>'+
                        '         <li><a name="top-a" id="suspend">suspend</a></li>'+
                        '     </ul>'+
                        '</li>'+
                        '<li><a name="top-a" id="second-menu" title="用户设置">用户设置</a>'+
                        '     <ul>'+
                        '         <li><a name="top-a" id="overloads">超量查询</a></li>'+
                        '         <li><a name="top-a" id="regexconfig">正则配置</a></li>'+
                        '         <li><a name="top-a" id="keycustomermonitor">重点用户监控</a></li>'+
                        '         <li><a name="top-a" id="channelignore">忽略大小写频道</a></li>'+
                        '     </ul>'+
                        '</li>'+
                        '<li><a name="top-a" id="logout">Logout</a>'+
                        '</li>';
   if(roles=="admin"){
        html += '<li>&nbsp<li>';
        html += '<li><a name="top-a" id="second-menu" title="用户设置">用户设置</a>'+
                        '     <ul>'+
                        '         <li><a name="top-a" href="config_adminuser.html">用户管理</a> <li>'+
                        '         <li><a name="top-a" id="requestway">request跟踪</a> <li>'+
                        '     </ul>'+
                        '</li>';
    }
        html +=         '</ul>';
    $("#navigate").html(html);
    $("a").css({"cursor":"pointer"});
}
function changeNavigate(){
    var id = $(this).attr("id");
    if(id=="index"){
        initIndexHtml();
    }
    if(id=="refresh_detail"){
        initRefreshDetailContent();
    }
    if(id=="error_task"){
        initErrorTaskHtml();
    }
    if(id=="clear_blacklist"){
        initClearBlackListHtml();
    }
    if(id=="overloads"){
        initOverloadsHtml();
    }
    if(id=="timeouts"){
        initTimeOutsHtml();
    }
    if(id=="rewrite"){
        initRewriteHtml();
    }
    if(id=="regexconfig"){
        initRegexConfigHtml();
    }
    if(id=="channelignore"){
        initChannelignoreHtml();
    }
    if(id=="keycustomermonitor"){
        initKeyCustomersMonitorHtml();
    }
    if(id=="suspend"){
        initSuspendHtml();
    }
    if(id=="logout"){
        location.href="/logout";
    }
    if(id=="requestway"){
        initRequestWayHtml();
        //alert("requestway");
    }
}
function startWait(){
    xval=getBusyOverlay(
    'viewport',
    {
        color:'black',
        opacity:0.5, 
        text:'正在加载,请耐心等待...', 
        style:'text-shadow: 0 0 3px black;font-weight:bold;font-size:16px;color:white'
    },
    {
        color:'#fff', 
        size:100, 
        type:'o'
    });
    return xval
}
function stopWait(){
    try{
        xval.remove();
        xval='';
    }catch(err){
        
    }
}
