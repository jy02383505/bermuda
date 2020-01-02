
function initIndexHtml(){
	var html = "<div><table id='mytable'>"+
	        	"</table></div>"+
	        	"<hr><div style='padding-left:30%;' id='refreshDetailCharts'></div><div id='refreshDetailCharts2'></div>";
	$("#content").html(html);
      $("h1").text(" 刷 新 系 统 首 页");
	    var dataUrl = "/getQueueCelery";
      getDataAjax(dataUrl,processDataIndex,"GET");
}
function processDataIndex(data){
  var right = $("#userInfo").attr("name");            
  var tablestr = "<tr>"+
        "<th width='20%'>服务器</th>"+
        "<th>celery状态</th>"+
        "<th>url_queue</th>"+
        "<th>celery</th>"+
        "<th>refresh</th>"+
        "<th>retry_queue</th>";
  if (right == "admin"){
        tablestr += "<th>操作</th>";
      }
    tablestr += "</tr>";
  $.each(data,function(index, entry) {
    try{
      tablestr += "<tr>"
               + "<td>"+entry["_id"]+"</td>"
               + "<td><span class='"+entry["celeryStatus"]+"'>"+entry["celeryStatus"]+"</span></td>";
               var urlQueueHtml = "", celeryHtml = "", refreshHtml = "", retryQueueHtml = "";
               $.each(entry["status"],function(s_index,s_entry){
                    if(s_entry['name'] == 'url_queue'){
                        urlQueueHtml = s_entry['m_ready'];
                    }
                    if(s_entry['name'] == 'celery'){
                        celeryHtml = s_entry['m_ready'];
                    }
                    if(s_entry['name'] == 'refresh'){
                        refreshHtml = s_entry['m_ready'];
                    }
                    if(s_entry['name'] == 'retry_queue'){
                        retryQueueHtml = s_entry['m_ready'];
                    }
               });

      tablestr += "<td>"+urlQueueHtml+"</td>"
               + "<td>"+celeryHtml+"</td>"
               + "<td>"+refreshHtml+"</td>"
               + "<td>"+retryQueueHtml+"</td>";
               if(right == "admin"){
                 initRefreshCharts();
                 tablestr += "<td><span id='option_"+entry["_id"]+"'>"
                 + "<a class='action' value='start'>start</a>  &nbsp;&nbsp;"
                 + "<a class='action' value='stop'>stop</a> &nbsp;&nbsp; "
                 + "<a class='action' value='restart'>restart</a>"
                 + "</span></td>";
               }
      tablestr += "<tr>";
    }catch(err){
      alert("initIndextable error:" + err)
    }
  });
  $("#mytable").append(tablestr);
  $(".action").click(function(){
      var action = $(this).attr("value");
      var host = $(this).parent().parent().parent().find("td:first").text();
      startWait();
      $.ajax({
          type: "GET",
          url: "/celery/"+host+"/"+action+"/",
          statusCode: {
              500: function() {
                alert("server error");
                location.href="/index.html";
              }
          },
          success: function(data){
              try{
                  alert(data);
                  location.href="/index.html";
              }catch(err){
                 alert(err);
                 stopWait(); 
              }finally{
                  stopWait();
              }

          }
      });
  });
}

function initRefreshCharts(){

$.ajax({
        type: "GET",
        url: "/refreshChartsData",
        statusCode: {
            500: function() {
              alert("server error");
              location.href="/index.html";
            }
        },
        success: function(data){
            try{
                 $("#refreshDetailCharts").insertFusionCharts({
                   swfUrl: "Pie3D.swf", 
                   dataSource: data, 
                   dataFormat: "json", 
                   width: "600", 
                   height: "400", 
                   id: "myChartId"
                }); 
            }catch(err){
               alert(err);
               stopWait(); 
            }finally{
                stopWait();
            }

        }
    });
}
