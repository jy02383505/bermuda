#router test data
from bson.objectid import ObjectId
from datetime import datetime


USERS='[{ "code": "2275", "companyName": "test", "name": "test", "password": "test", "userState": "TEST" }]'
CHANNELS='[{ "billingCode": "38342", "channelState": "COMMERCIAL", "code": "53831", "customerCode": "2275", "customerName": "test", "multilayer": true, "name": "http://test.com.cn", "productCode": "34", "transferTime": "" }]'
CHANNEL_MONGO={ "billingCode": "38342", "channelState": "COMMERCIAL", "code": "53831", "customerCode": "2275", "customerName": "test", "multilayer": True, "name": "http://test.com.cn", "productCode": "34", "transferTime": "" }
CUSTOMER='{ "channels": [], "code": "2275", "companyName": "", "enable": true, "name": "test", "password": "", "userState": "TEST" }'
DEVICES='devices:[{      "status" : "SUSPEND",      "name" : "PBL-DG-6-3C4",      "serialNumber" : "25076963C4",      "host" : "112.90.217.102",      "firstLayer" : false,      "port" : 21108    }]'
CUSTOMER_PORTAL='[{"accountType":"0","apipwd":"workercn@123","customerCode":"2754","name":"workercn","password":"","status":"commercial"}]'
CHANNELS_PORTAL='{"businesses":[{"businessId":5120165,"productCode":"9040200000452","businessCnName":"BGP","businessEnName":"Zhaowei-Uni 8 Lines BGP","billType":"max(in,out)","productType":"main","regions":[{"regionId":9050,"regionCnName":"chinaarea","regionEnName":"Mainland China "}],"billingUnits":[{"billingUnitId":"7484","billingUnitName":"idc://bgp.workercn.com"}],"channels":[{"channelId":"15159","channelName":"idc://bgp.workercn.com"},{"channelId":"60093","channelName":"idc://bgp.workercn1.com"}]}]}'
CHANNEL_PORTAL_MONGO={"username" : "workercn",  "channels" : [{"channelName" : "idc://bgp.workercn.com",      "channelId" : "15159"    }, {      "channelName" : "idc://bgp.workercn1.com",      "channelId" : "60093"}],  "needUpdateRedis" : False,  "userinfo" : {    "status" : "commercial",    "customerCode" : "2754",    "name" : "workercn",    "accountType" : "0",    "mainUsername" : "workercn"  },  "time" : "2014-11-10 13:08:59.623913"}


# if __name__ == '__main__':
#     print RESPONSE_BODY.split('\r\n\r\n')[1]
#     print 24*8+43*3+36+441

