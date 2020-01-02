#router test data
from bson.objectid import ObjectId
from datetime import datetime

ONE_LAYER = "one"
TWO_LAYER = "two"
THREE_LAYER = "three"
   
MESSAGES_THREE = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler3/fuck3.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'three'
    }
] 
MERGED_URL_THREE = {
        '19297': [ 
        {
            'status': 'PROGRESS', 
            'isdir': False, 
            'ignore_case': False, 
            'id': '4e4c7b9f5bc89412ec000004', 
            'username': 'snda', 
            'url': u'http://dl.autopatch.ccgslb.net/cooler3/fuck3.jpg', 
            'r_id': '512ed15e414ec06479575561', 
            'action': 'purge', 
            'firstLayer': True, 
            'channel_code': '19297',
            'layer_type':'three'
        }
    ]
}

MESSAGES_TWO = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler2/fuck2.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'two'
    }
] 
MERGED_URL_TWO = {
        '19297': [ 
        {
            'status': 'PROGRESS', 
            'isdir': False, 
            'ignore_case': False, 
            'id': '4e4c7b9f5bc89412ec000004', 
            'username': 'snda', 
            'url': u'http://dl.autopatch.ccgslb.net/cooler2/fuck2.jpg', 
            'r_id': '512ed15e414ec06479575561', 
            'action': 'purge', 
            'firstLayer': True, 
            'channel_code': '19297',
            'layer_type':'two'
        }
    ]
}

MESSAGES_ONE = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'one'
    }
]
 
MERGED_URL_ONE = {
        '19297': [ 
        {
            'status': 'PROGRESS', 
            'isdir': False, 
            'ignore_case': False, 
            'id': '4e4c7b9f5bc89412ec000004', 
            'username': 'snda', 
            'url': u'http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg', 
            'r_id': '512ed15e414ec06479575561', 
            'action': 'purge', 
            'firstLayer': False, 
            'channel_code': '19297',
            'layer_type':'one'
        }
    ]
}

PRELOAD_MESSAGES = [
    { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'TIMER',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '1',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': '2014-11-01 00:00:00',
        'created_time': '2014-12-01 00:00:00'
    }, { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '1',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': '2014-11-01 00:00:00',
        'created_time': '2014-12-01 00:00:00'
    }, { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '2',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck2.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': '2014-11-01 00:00:00',
        'created_time': '2014-12-01 00:00:00'
    }, { 
        '_id' : '5438ffa325b541639c37f84d',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '3',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-cdn.ymapp.com/app/fuck3.apk',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '5438ffa325b541639c37f83f',
        'is_multilayer' : True,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56659',
        'start_time': '2014-11-01 00:00:00',
        'created_time': '2014-12-01 00:00:00'
    }
]

PRELOAD_MESSAGES_PROGRESS = [
    { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '1',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': '2014-11-01 00:00:00',
        'created_time': datetime(2014, 12, 1, 0, 0)
    }, { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '2',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck2.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': '2014-11-01 00:00:00',
        'created_time': datetime(2014, 12, 1, 0, 0)
    }, { 
        '_id' : '5438ffa325b541639c37f84d',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '3',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-cdn.ymapp.com/app/fuck3.apk',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '5438ffa325b541639c37f83f',
        'is_multilayer' : True,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56659',
        'start_time': '2014-11-01 00:00:00',
        'created_time': datetime(2014, 12, 1, 0, 0)
    }
]

PRELOAD_MESSAGES_URL = {
    '56634': [
        { 
            '_id' : '543a906a25b541639c380ac2',
            'username' : 'youmi',
            'parent': 'youmi',
            'status' : 'PROGRESS',
            'get_url_speed' : '1024k',
            'user_id' : '4648',
            'check_type' : 'BASIC',
            'task_id' : '1',
            'remote_addr' : '115.231.94.72',
            'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
            'preload_address' : '127.0.0.1:80',
            'priority' : 0,
            'nest_track_level' : 0,
            'dev_id' : '543a906a25b541639c380ac1',
            'is_multilayer' : False,
            'action' : 'refresh,preload',
            'md5' : '',
            'channel_code' : '56634',
            'start_time': '2014-11-01 00:00:00',
            'created_time': datetime(2014, 12, 1, 0, 0)
        }, { 
            '_id' : '543a906a25b541639c380ac2',
            'username' : 'youmi',
            'parent': 'youmi',
            'status' : 'PROGRESS',
            'get_url_speed' : '1024k',
            'user_id' : '4648',
            'check_type' : 'BASIC',
            'task_id' : '2',
            'remote_addr' : '115.231.94.72',
            'url' : u'http://owan-img.ymapp.com/img/fuck2.jpg',
            'preload_address' : '127.0.0.1:80',
            'priority' : 0,
            'nest_track_level' : 0,
            'dev_id' : '543a906a25b541639c380ac1',
            'is_multilayer' : False,
            'action' : 'refresh,preload',
            'md5' : '',
            'channel_code' : '56634',
            'start_time': '2014-11-01 00:00:00',
            'created_time': datetime(2014, 12, 1, 0, 0)
        }
    ],
    '56659' : [
        { 
            '_id' : '5438ffa325b541639c37f84d',
            'username' : 'youmi',
            'parent': 'youmi',
            'status' : 'PROGRESS',
            'get_url_speed' : '1024k',
            'user_id' : '4648',
            'check_type' : 'BASIC',
            'task_id' : '3',
            'remote_addr' : '115.231.94.72',
            'url' : u'http://owan-cdn.ymapp.com/app/fuck3.apk',
            'preload_address' : '127.0.0.1:80',
            'priority' : 0,
            'nest_track_level' : 0,
            'dev_id' : '5438ffa325b541639c37f83f',
            'is_multilayer' : True,
            'action' : 'refresh,preload',
            'md5' : '',
            'channel_code' : '56659',
            'start_time': '2014-11-01 00:00:00',
            'created_time': datetime(2014, 12, 1, 0, 0)
        }
    ]
}

PRELOAD_MESSAGES_TIMER = [
    { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'TIMER',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '1',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': datetime(2014, 11, 1, 0, 0),
        'created_time': datetime(2014, 12, 1, 0, 0)
    }
]

PRELOAD_MESSAGES_TIMER_PROGRESS = [
    { 
        '_id' : '543a906a25b541639c380ac2',
        'username' : 'youmi',
        'parent': 'youmi',
        'status' : 'PROGRESS',
        'get_url_speed' : '1024k',
        'user_id' : '4648',
        'check_type' : 'BASIC',
        'task_id' : '1',
        'remote_addr' : '115.231.94.72',
        'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
        'preload_address' : '127.0.0.1:80',
        'priority' : 0,
        'nest_track_level' : 0,
        'dev_id' : '543a906a25b541639c380ac1',
        'is_multilayer' : False,
        'action' : 'refresh,preload',
        'md5' : '',
        'channel_code' : '56634',
        'start_time': datetime(2014, 11, 1, 0, 0),
        'created_time': datetime(2014, 11, 1, 0, 0)
    }
]

MESSAGES = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler3/fuck3.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'three'
    },{
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler2/fuck2.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'three'
    },
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19298',
        'layer_type':'three'
    }]

MERGED_URL = {
        '19297': [ 
        {
            'status': 'PROGRESS', 
            'isdir': False, 
            'ignore_case': False, 
            'id': '4e4c7b9f5bc89412ec000004', 
            'username': 'snda', 
            'url': u'http://dl.autopatch.ccgslb.net/cooler3/fuck3.jpg', 
            'r_id': '512ed15e414ec06479575561', 
            'action': 'purge', 
            'firstLayer': True, 
            'channel_code': '19297',
            'layer_type':'three'
        },
        {
            'status': 'PROGRESS', 
            'isdir': False, 
            'ignore_case': False, 
            'id': '4e4c7b9f5bc89412ec000004', 
            'username': 'snda', 
            'url': u'http://dl.autopatch.ccgslb.net/cooler2/fuck2.jpg', 
            'r_id': '512ed15e414ec06479575561', 
            'action': 'purge', 
            'firstLayer': True, 
            'channel_code': '19297',
            'layer_type':'three'
        }],
        '19298': [
        {
            'status': 'PROGRESS', 
            'isdir': False, 
            'ignore_case': False, 
            'id': '4e4c7b9f5bc89412ec000004', 
            'username': 'snda', 
            'url': u'http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg', 
            'r_id': '512ed15e414ec06479575561', 
            'action': 'purge', 
            'firstLayer': True, 
            'channel_code': '19298',
            'layer_type':'three'
        }
        ]
    }

MESSAGES_DIR = [
    {
        'status': 'PROGRESS', 
        'isdir': True, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler3/', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'three'
    },{
        'status': 'PROGRESS', 
        'isdir': True, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler2/', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'two'
    },
    {
        'status': 'PROGRESS', 
        'isdir': True, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler1/', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': False, 
        'channel_code': '19297',
        'layer_type':'one'
        }]

URL_LIST_THREE = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler3/fuck3.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'three',
        'dev_id':'4e79a53c815c5e25fe001228',
    }
]

URL_LIST_TWO = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler2/fuck2.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': True, 
        'channel_code': '19297',
        'layer_type':'two',
        'dev_id':'4e79a53c815c5e25fe001228',
    }
]

URL_LIST_ONE = [
    {
        'status': 'PROGRESS', 
        'isdir': False, 
        'ignore_case': False, 
        'id': '4e4c7b9f5bc89412ec000004', 
        'username': 'snda', 
        'url': u'http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg', 
        'r_id': '512ed15e414ec06479575561', 
        'action': 'purge', 
        'firstLayer': False, 
        'channel_code': '19297',
        'layer_type':'one',
        'dev_id':'4e79a53c815c5e25fe001228',
    }
]

URL_DEVS_MUL=[{'status': 'OPEN', 'name': 'CHN-WZ-V-3C5', 'serialNumber': '010577V3C5', 'host': '61.164.154.249', 'firstLayer': False, 'port': 21108}, {'status': 'OPEN', 'name': 'CNC-ZZ-3-3C2', 'serialNumber': '06037133C2', 'host': '61.158.249.2', 'firstLayer': False, 'port': 21108}, {'status': 'OPEN', 'name': 'CHN-WZ-V-3C6', 'serialNumber': '010577V3C6', 'host': '61.164.154.249', 'firstLayer': True, 'port': 21108}, {'status': 'OPEN', 'name': 'CNC-ZZ-3-3C1', 'serialNumber': '06037133C1', 'host': '61.158.249.2', 'firstLayer': True, 'port': 21108}]
########################----for dir
DIR_THREE = {
    'status': 'PROGRESS', 
    'isdir': True, 
    'ignore_case': False, 
    'id': '4e4c7b9f5bc89412ec000004', 
    'username': 'snda', 
    'url': u'http://dl.autopatch.ccgslb.net/cooler3/', 
    'r_id': '512ed15e414ec06479575561', 
    'action': 'purge', 
    'firstLayer': True, 
    'channel_code': '19297',
    'layer_type':'three'
}


DIR_TWO = {
    'status': 'PROGRESS', 
    'isdir': True, 
    'ignore_case': False, 
    'id': '4e4c7b9f5bc89412ec000004', 
    'username': 'snda', 
    'url': u'http://dl.autopatch.ccgslb.net/cooler2/', 
    'r_id': '512ed15e414ec06479575561', 
    'action': 'purge', 
    'firstLayer': True, 
    'channel_code': '19297',
    'layer_type':'two'
}


DIR_ONE =  {
    'status': 'PROGRESS', 
    'isdir': True, 
    'ignore_case': False, 
    'id': '4e4c7b9f5bc89412ec000004', 
    'username': 'snda', 
    'url': u'http://dl.autopatch.ccgslb.net/cooler1/', 
    'r_id': '512ed15e414ec06479575561', 
    'action': 'purge', 
    'firstLayer': False, 
    'channel_code': '19297',
    'layer_type':'one'
}


#######################
DEV_ID = ObjectId("4e79a53c815c5e25fe001228")

LAYER_DEVICES = [ 
    {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C6', 
        'serialNumber': '010577V3C6', 
        'host': '61.164.154.249', 
        'firstLayer': True, 
        'port': 21108
    },
    {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C1', 
        'serialNumber': '06037133C1', 
        'host': '61.158.249.2', 
        'firstLayer': True, 
        'port': 21108
    }]

LAYER_DB_DEV_DICT ={"CHN-WZ-V-3C6": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C6', 
        'serialNumber': '010577V3C6', 
        'host': '61.164.154.249', 
        'firstLayer': True, 
        'port': 21108,
        'code' :0
    },
        "CNC-ZZ-3-3C1": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C1', 
        'serialNumber': '06037133C1', 
        'host': '61.158.249.2', 
        'firstLayer': True, 
        'port': 21108,
        'code' :0
    }}

DB_MULTILAYER_DEV_DICT= {"CHN-WZ-V-3C6": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C6', 
        'serialNumber': '010577V3C6', 
        'host': '61.164.154.249', 
        'firstLayer': True, 
        'port': 21108,
        'code' :0
    },
        "CNC-ZZ-3-3C1": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C1', 
        'serialNumber': '06037133C1', 
        'host': '61.158.249.2', 
        'firstLayer': True, 
        'port': 21108,
        'code' :0
    },"CHN-WZ-V-3C5": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108,
        'code' :0
    },
        "CNC-ZZ-3-3C2": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108,
        'code' :0
        }
    }

DB_MULTILAYER_DEV_DICT_HALF= {"CHN-WZ-V-3C6": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C6', 
        'serialNumber': '010577V3C6', 
        'host': '61.164.154.249', 
        'firstLayer': True, 
        'port': 21108,
        'code' :200
    },
        "CNC-ZZ-3-3C1": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C1', 
        'serialNumber': '06037133C1', 
        'host': '61.158.249.2', 
        'firstLayer': True, 
        'port': 21108,
        'code' :200
    },"CHN-WZ-V-3C5": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108
    },
        "CNC-ZZ-3-3C2": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108}
    }

DB_MULTILAYER_DEV_DICT_FINISHED = {"CHN-WZ-V-3C6": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C6', 
        'serialNumber': '010577V3C6', 
        'host': '61.164.154.249', 
        'firstLayer': True, 
        'port': 21108,
        'code' :200
    },
        "CNC-ZZ-3-3C1": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C1', 
        'serialNumber': '06037133C1', 
        'host': '61.158.249.2', 
        'firstLayer': True, 
        'port': 21108,
        'code' :200
    },"CHN-WZ-V-3C5": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108,
        'code' :200
    },
        "CNC-ZZ-3-3C2": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108,
        'code' :200}
    }

DB_MULTILAYER_DEV = {"_id":ObjectId(DEV_ID), 
"devices": DB_MULTILAYER_DEV_DICT, "unprocess": 4, "created_time": datetime(2012, 1, 1, 0, 1, 0, 000000)}

DB_MULTILAYER_DEV_HALF = {"_id":ObjectId(DEV_ID), 
"devices": DB_MULTILAYER_DEV_DICT_HALF, "unprocess": 2, "created_time": datetime(2012, 1, 1, 0, 1, 0, 000000)}

DB_MULTILAYER_DEV_FINISHED = {"_id":ObjectId(DEV_ID), 
"devices": DB_MULTILAYER_DEV_DICT_FINISHED, "unprocess": 0, "created_time": datetime(2012, 1, 1, 0, 1, 0, 000000), "finish_time": datetime(2012, 1, 1, 0, 1, 0, 000000)}


LOWER_DEVICES = [ 
    {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108
    },
    {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108
    }]

DEVICES = [ 
    {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108
    },
    {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108
    }]

FAILURE_DEVICES = [
    {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108
    }
]

DEVICES_MAP = {
    "61.158.249.2":
    {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108
    },
    "61.164.154.249":
     {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108
    }
}

FAILURE_DEVICES_MAP = {
    "61.158.249.2":
    {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108
    }
}

DB_DEV_DICT ={"CHN-WZ-V-3C5": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108,
        'code' :0
    },
        "CNC-ZZ-3-3C2": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108,
        'code' :0
    }}
DB_DEV_DICT_FINISHED ={"CHN-WZ-V-3C5": {
        'status': 'OPEN', 
        'name': 'CHN-WZ-V-3C5', 
        'serialNumber': '010577V3C5', 
        'host': '61.164.154.249', 
        'firstLayer': False, 
        'port': 21108,
        'code' :200
    },
        "CNC-ZZ-3-3C2": {
        'status': 'OPEN', 
        'name': 'CNC-ZZ-3-3C2', 
        'serialNumber': '06037133C2', 
        'host': '61.158.249.2', 
        'firstLayer': False, 
        'port': 21108,
        'code' :200
    }}
    
DB_DEV = {"_id":ObjectId(DEV_ID), 
"devices": DB_DEV_DICT, "unprocess": 2, "created_time": datetime(2012, 1, 1, 0, 1, 0, 000000)}

DB_FINISHED_DEV = {"_id":ObjectId(DEV_ID), 
"devices": DB_DEV_DICT_FINISHED, "unprocess": 0, "created_time": datetime(2012, 1, 1, 0, 1, 0, 000000), "finish_time": datetime(2012, 1, 1, 0, 1, 0, 000000)}


####################### 
COMMAND_HEAD = '<?xml version="1.0" encoding="utf-8"?>'
COMMAND_METHOD_BEGIN = '<method name="url_purge" sessionid="e4e2014f8d1211e18dc200247e10b29b">'
COMMAND_RECURSION = '<recursion>0</recursion>' 
COMMAND_URL_LIST_BEGIN = '<url_list>'
COMMAND_URL_THREE = '<url id="0">http://dl.autopatch.ccgslb.net/cooler3/fuck3.jpg</url>'
COMMAND_URL_TWO = '<url id="0">http://dl.autopatch.ccgslb.net/cooler2/fuck2.jpg</url>'
COMMAND_URL_ONE = '<url id="0">http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg</url>'
COMMAND_URL_LIST_END = '</url_list>'
COMMAND_METHOD_END = '</method>'

COMMAND_URL_LIST_ONE = COMMAND_HEAD + COMMAND_METHOD_BEGIN + COMMAND_RECURSION + COMMAND_URL_LIST_BEGIN + COMMAND_URL_ONE + COMMAND_URL_LIST_END + COMMAND_METHOD_END
COMMAND_DIR_LIST_ONE='<method name="dir_purge" sessionid="e4e2014f8d1211e18dc200247e10b29b"><action>0</action><dir>http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg</dir><report_address>localhost</report_address></method>'
DOLOOP_RESULT_SUCCESS = [
    '61.164.154.249\r\n<?xml version="1.0" encoding="UTF-8"?>\r\n<url_purge_response sessionid="089790c08e8911e1910800247e10b29b">\r\n<url_ret id="0">200</url_ret>\r\n</url_purge_response>', 
    '61.158.249.2\r\n<?xml version="1.0" encoding="UTF-8"?>\r\n<url_purge_response sessionid="089790c08e8911e1910800247e10b29d">\r\n<url_ret id="0">200</url_ret>\r\n</url_purge_response>'
    ]
DOLOOP_RESULT_FAILURE = [
    '61.164.154.249\r\n<?xml version="1.0" encoding="UTF-8"?>\r\n<url_purge_response sessionid="089790c08e8911e1910800247e10b29b">\r\n<url_ret id="0">200</url_ret>\r\n</url_purge_response>', 
    '61.158.249.2\r\n<?xml version="1.0" encoding="UTF-8"?>\r\n<url_purge_response sessionid="089790c08e8911e1910800247e10b29d">\r\n<url_ret id="0">404</url_ret>\r\n</url_purge_response>'
    ]

DOLOOP_RETRY_RESULT_SUCCESS = [
    '61.158.249.2\r\n<?xml version="1.0" encoding="UTF-8"?>\r\n<url_purge_response sessionid="089790c08e8911e1910800247e10b29d">\r\n<url_ret id="0">200</url_ret>\r\n</url_purge_response>'
    ]
DOLOOP_RETRY_RESULT_FAILURE= [
    '61.158.249.2\r\n<?xml version="1.0" encoding="UTF-8"?>\r\n<url_purge_response sessionid="089790c08e8911e1910800247e10b29d">\r\n<url_ret id="0">404</url_ret>\r\n</url_purge_response>'
    ]

DO_SEND_URL_SUCCESS_RESULT = [
    {
        'code': 200, 
        'host': '61.164.154.249', 
        'firstLayer': False, 'name': 
        'CHN-WZ-V-3C5'
    }
]

DO_SEND_URL_FIRST_RESULT_FAILURE = [
    {
        "code": 404, 
        "host": "61.158.249.2", 
        "firstLayer": False, 
        "name": "CNC-ZZ-3-3C2"
    }
]

RET_FAILURE_DEVICES_MAP =  {
    "61.158.249.2":{
        'code': 503, 'name': 'CNC-ZZ-3-3C2',
                  'total_cost': 0, 'connect_cost': 0,
                  'host': '61.158.249.2', 'response_cost': 0,
                  'firstLayer': False
    }
}
DO_SEND_URL_RESULT_1 = [
    {'code': 503, 'name': 'CHN-WZ-V-3C5', 'total_cost': 0, 'connect_cost': 0, 'host': '61.164.154.249',
     'response_cost': 0, 'firstLayer': False},
    {'code': 503, 'name': 'CNC-ZZ-3-3C2', 'total_cost': 0, 'connect_cost': 0, 'host': '61.158.249.2',
     'response_cost': 0, 'firstLayer': False}]


DO_SEND_URL_RESULT = [
    {
        "code": 200, 
        "host": "61.164.154.249", 
        "firstLayer": False, 
        "name": "CHN-WZ-V-3C5"
    },
    {
        "code": 200, 
        "host": "61.158.249.2", 
        "firstLayer": False, 
        "name": "CNC-ZZ-3-3C2"
    }
]


DO_SEND_URL_RESULT_FAILURE = [
    {
        "code": 200, 
        "host": "61.164.154.249", 
        "firstLayer": False, 
        "name": "CHN-WZ-V-3C5"
    },
    {
        "code": 404, 
        "host": "61.158.249.2", 
        "firstLayer": False, 
        "name": "CNC-ZZ-3-3C2"
    }
]

RESPONSE_BODY = 'HTTP/1.0 200 OK\r\n\
Content-Length: 186\r\n\
\r\n\
<?xml version="1.0" encoding="UTF-8"?>\r\n\
<url_purge_response sessionid="966c22dc8ac111e2963fbcaec50f6e14">\r\n\
<url_ret id="1">200</url_ret>\r\n\
\r\n\
</url_purge_response>'

URL_XML_BODY = '<?xml version="1.0" encoding="UTF-8"?>\r\n\
<url_purge_response sessionid="702542e0904611e2963fbcaec50f6e14">\r\n\
<url_ret id="0">200</url_ret>\r\n\
</url_purge_response>'
DIR_XML_BODY = '<?xml version="1.0" encoding="UTF-8"?>\
<dir_expire_response sessionid="38c3b76e904611e2963fbcaec50f6e14">\
<ret>200</ret>\
</dir_expire_response>'


splitter_new_urls = [{
                "_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "url":"http://www.chinacache.com/a.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"purge",
                "firstLayer":False, "is_multilayer":False,
                "channel_code":'0005'},
                { "_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "url":"http://www.chinacache.com/",
                "status":"PROGRESS",
                "isdir":True,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False, "is_multilayer":False,
                "channel_code":'0005'},
                { "_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "url":"http://www.chinacache.com/u.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False, "is_multilayer":False,
                "channel_code":'0005'},
        { "_id":ObjectId("4e4c7b9f5bc89412ec000004"),
        "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
        "url":"http://www.chinacache.com/c.jpg",
        "status":"PROGRESS",
        "isdir":False,
        "username":"chinacache",
        "action":"preload",
        "firstLayer":False,
        "is_multilayer":False,
        "channel_code":'0005'}]
splitter_new_url_list = [{
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/a.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"purge",
                "firstLayer":False,
                "channel_code":'0005'},
                {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/",
                "status":"PROGRESS",
                "isdir":True,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False,
                "channel_code":'0005'},
                {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/u.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False,
                "channel_code":'0005'}, {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/c.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"preload",
                "firstLayer":False,
                "channel_code":'0005'}]
do_send_dir_url={
        'status': 'PROGRESS',
        'isdir': False,
        'ignore_case': False,
        'id': '4e4c7b9f5bc89412ec000004',
        'username': 'snda',
        'url': u'http://dl.autopatch.ccgslb.net/cooler1/fuck1.jpg',
        'r_id': '512ed15e414ec06479575561',
        'action': 'purge',
        'firstLayer': False,
        'channel_code': '19297',
        'layer_type':'one',
        'dev_id':'4e79a53c815c5e25fe001228',
    }
do_send_dir_dev=[


]


