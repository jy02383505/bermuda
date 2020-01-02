function checkBrowser(){
    if($.browser.safari || $.browser.mozilla || $.browser.opera){
        return true;
    }
    if($.browser.msie && parseInt($.browser['version'])>=9){
        return true;
    }
}
if (!checkBrowser()){
    var text = "<h1 style='color:white;'>请选用谷歌、火狐、opera或ie9以上版本浏览器！</h1>" ;
    $("#warp").html(text);
}else{

    var remember = $.cookie('remember');
    if (remember == 'true') 
    {
        var username = $.cookie('username');
        var password = $.cookie('password');
        // autofill the fields
        $('#username').val(username);
        $('#password').val(password);
    }
    $("#refresh-msg-dialog").dialog({
            autoOpen: false,
            width: 260,
            height: 130,
            resizable:"false",
            modal: true,
            buttons: [
                {
                    text: "Ok",
                    click: function() {
                        $(this).dialog("close");
                        $("#refresh-msg").html("");
                    }
                }
            ]
    });
    $("#refresh").click(function(event) {
    	var username = $("#username").val().trim();
    	var password = $("#password").val().trim();
        if ($('#remember').is(':checked')) {
            // set cookies to expire in 14 days
            $.cookie('username', username, { expires: 14 });
            $.cookie('password', password, { expires: 14 });
            $.cookie('remember', true, { expires: 14 });                
        }
        else
        {
            // reset cookies
            $.cookie('username', null);
            $.cookie('password', null);
            $.cookie('remember', null);
        }
		if(username == ""){
			var text = "username不能都为空！" 
        	$("#refresh-msg").html(text);
        	$("#refresh-msg-dialog").dialog("open");
    		return;
		}
		if(password == ""){
			var text = "password不能都为空！" 
        	$("#refresh-msg").html(text);
        	$("#refresh-msg-dialog").dialog("open");
    		return;
		}
    	if($("#urls").val().trim() == "" && $("#dirs").val().trim() == "" ){
		    var text = "URLS和DIRS不能都为空！" 
        	$("#refresh-msg").html(text);
        	$("#refresh-msg-dialog").dialog("open");
    		return;
    	}
    	var urlsArr = $("#urls").val().trim().split("\n");
    	var dirsArr = $("#dirs").val().trim().split("\n");
		var urls = '["'+urlsArr.join('","')+'"]';
		var dirs = '["'+dirsArr.join('","')+'"]';
		xval=getBusyOverlay(
		'viewport',
		{
			color:'black',
			opacity:0.5, 
			text:'refresh: waiting result...', 
			style:'text-shadow: 0 0 3px black;font-weight:bold;font-size:16px;color:white'
		},
		{
			color:'#fff', 
			size:156, 
			type:'o'
		});
    	$.ajax({
            type: "POST",
            url: "/content/refresh",
            data:{'username': username, 'password': password, 'task': '{"urls":'+urls+',"dirs":'+dirs+'}'},
            statusCode: {
                403: function(data) {
                	xval.remove();xval='';
        		    var text = data['responseText']; 
			    	$("#refresh-msg").html(text);
			    	$("#refresh-msg-dialog").dialog("open");
					event.preventDefault();
                },
                400: function(data) {
                	xval.remove();xval='';
        		    var text = data['responseText']; 
			    	$("#refresh-msg").html(text);
			    	$("#refresh-msg-dialog").dialog("open");
					event.preventDefault();
                },
                500: function(data) {
                	xval.remove();xval='';
        		    var text = data['responseText']; 
			    	$("#refresh-msg").html(text);
			    	$("#refresh-msg-dialog").dialog("open");
					event.preventDefault();
                }
            },
            success: function(data){
            	xval.remove(); xval='';
            	var text = "请求提交成功！" 
            	$("#refresh-msg").html(text);
            	$("#refresh-msg-dialog").dialog("open");
        		event.preventDefault();
                }
        });
    });

}