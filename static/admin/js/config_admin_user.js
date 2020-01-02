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
        $("body").css({"background-color":"#555","text-align":"center"});
    }else{
         $.ajax({
            type: "GET",
            url: "/getUserInfo",
            success: function(data){
                if(data['userInfo']['roles'] != "admin"){
                    alert("您无权查看该网页");
                    location.href="/login.html";
                }else {
                    getUserList();
                }
            }
        });
    }
    function getUserList(){
        $.ajax({
            type: "GET",
            url: "/admin_userList",
            success: function(data){
                var html = "";
                $.each(data['admin_userList'],function(index,entry){
                    html += "<tr>"+
                            "<td><a class='a_update' style='cursor:pointer;'>"+entry['_id']+"</a></td>"+
                            "<td>"+entry['right']+"</td>"+
                            "<td><a class='del'>删除</a></td>"+
                            "</tr>"
                });
                $("#mytable>tbody").html(html);
                if(data.length>0){
                    $("#mytable").tablesorter();
                }
                $("a.del").click(function(){
                    var userID = $(this).parent().prev().prev().find("a").html();
                    var right = $(this).parent().prev().text();
                    $.ajax({
                        type: "GET",
                        url: "/config_user",
                        data:{"userID":userID,"right":right,"operation":"del"},
                        success: function(data){
                            alert(data);
                            location.href="/config_adminuser.html";
                        }
                    });
                });
                $("a.a_update").click(function(){
                    $("#userID").val($(this).html());
                    $("#right").val($(this).parent().next().text());
                });
            }
        });
    }
