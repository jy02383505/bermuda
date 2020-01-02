package main

import (
	"fmt"
	// "log"
	"strconv"
	"sync"
	"time"
	// "Ultron/resources/redis"
	log "github.com/cihub/seelog"
	// "github.com/garyburd/redigo/redis"
	// "Ultron/internal/github.com/garyburd/redigo/redis"

	// _ "net/http/pprof"

	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"gopkg.in/redis.v3"
	// log "github.com/Sirupsen/logrus"
)

// var log log.LoggerInterface
type Device struct {
	Status     string `bson:"status"`
	Name       string `bson:"name"`
	Host       string `bson:"host"`
	FirstLayer string `bson:"firstLayer"`
	Code       int    `bson:"code"`
	A_code     int    `bson:"a_code"`
	R_code     int    `bson:"r_code"`
	B_code     int    `bson:"branch_code"`
}

//RBDevices is retry_device_branch
type RBDevices struct {
	Id          bson.ObjectId `bson:"_id"`
	RID         bson.ObjectId `bson:"rid"`
	UID         bson.ObjectId `bson:"uid"`
	Create_time time.Time     `bson:"create_time"`
	Deivces     []Device      `bson:"devices"`
}

type DDevices struct {
	Id      bson.ObjectId     `bson:"_id"`
	Deivces map[string]Device `bson:"devices"`
}

type Url struct {
	Id       bson.ObjectId `bson:"_id"`
	Status   string        `bson:"status"`
	Username string        `bson:"username"`
	// Ignore_case   bool          `bson:"ignore_case"`
	Parent string `bson:"parent"`
	// Is_multilayer bool          `bson:"is_multilayer"`
	// Isdir         bool          `bson:"isdir"`
	Url         string        `bson:"url"`
	Dev_id      bson.ObjectId `bson:"dev_id"`
	Create_time time.Time     `bson:"create_time"`
	// Type          string        `bson:"type"`
	// Action        string        `bson:"action"`
	Channel_code  int           `bson:"channel_code"`
	RetryBranchID bson.ObjectId `bson:"retry_branch_id"`
}

var uri string = fmt.Sprintf("mongodb://bermuda:bermuda_refresh@%s:27017/bermuda", "223.202.52.136")
var redisHost string = "223.202.52.82:6379"
var cacheDB int64 = 15
var goroutineNum = 500
var taskChannel = make(chan Url, 1000000)

var (
	redisClient  *redis.Client
	session      *mgo.Session
	databaseName = "bermuda"
)

// uri ='mongodb://bermuda:bermuda_refresh@%s:27017,%s:27017,%s:27017/bermuda?replicaSet=bermuda_db' % ('172.16.12.136', '172.16.12.135', '172.16.12.134')

func getUrls() []Url {
	var url_his []Url
	tt := time.Now()

	// st := tt.Add(time.Minute * 45)
	st := time.Date(tt.Year(), tt.Month(), tt.Day(), tt.Hour()-1, 0, 0, 0, time.UTC)
	// st := time.Date(tt.Year(), tt.Month(), tt.Day(), 0, 0, 0, 0, time.UTC)
	// et := st.Add(time.Hour)
	fromDate := st
	// fromDate := st.Add(time.Hour * 0)
	// fromDate := st.Add(time.Minute * 45)
	//toDate := st.Add(time.Minute * 15)
	toDate := st.Add(time.Hour * 1)
	// toDate := time.Date(et.Year(), et.Month(), et.Day(), et.Hour(), et.Minute(), 0, 0, time.UTC)
	log.Debug(fromDate, toDate)
	// find_url_dic = {"created_time": {"$gte": pre_time, "$lt": end_time},
	//                     "status": {"$ne": "INVALID"}}
	//     field_dic = {"username": 1, "_id": 1, "dev_id": 1, "channel_code": 1, "parent": 1, "url": 1, "status": 1,
	//                  "created_time": 1}
	// result := Url{}
	query := func(c *mgo.Collection) error {
		fn := c.Find(bson.M{"created_time": bson.M{"$gte": fromDate, "$lt": toDate}, "status": bson.M{"$ne": "INVALID"}}).All(&url_his)
		return fn
	}
	search := func() error {
		return withCollection("url", query)
	}
	// err := c.Find(bson.M{"created_time": bson.M{"$gte": fromDate, "$lt": toDate}, "status": bson.M{"$ne": "INVALID"}}).All(&url_his)
	// if err != nil {
	// 	log.Error(err)
	// }
	err := search()
	if err != nil {
		panic(err)
	}
	return url_his

}

func processFailedURL(u Url) error {
	result := DDevices{}
	resultRBD := RBDevices{}
	//retry_device_branch
	queryRBD := func(c *mgo.Collection) error {
		fn := c.Find(bson.M{"_id": u.RetryBranchID}).One(&resultRBD)
		return fn
	}
	searchRBD := func() error {
		return withCollection("retry_device_branch", queryRBD)
	}
	errRBD := searchRBD()
	if errRBD != nil {
		log.Error(u.RetryBranchID, errRBD, u, u.RetryBranchID)
	}

	//device
	query := func(c *mgo.Collection) error {
		fn := c.Find(bson.M{"_id": u.Dev_id}).One(&result)
		return fn
	}
	search := func() error {
		return withCollection("device", query)
	}
	err := search()
	if err != nil {
		log.Error(err)
		return err
	}

	// fmt.Println(datestr)
	SucessDevice := make(map[string]int)
	for _, d := range resultRBD.Deivces {
		if d.B_code == 200 {
			SucessDevice[d.Name] = d.B_code
		}
	}
	var code int = 200
	//11:00--12:00
	dd, _ := time.ParseDuration("-1h")
	tt := time.Now()
	datestr := fmt.Sprint(tt.Add(dd).Format("20060102"))
	for _, v := range result.Deivces {
		code_key := fmt.Sprintf("%s_%s", datestr, v.Name)
		// fmt.Println(code_key)
		if c, ok := SucessDevice[v.Name]; ok {
			code = c
		} else if v.Code == 503 {
			code = v.A_code
		} else {
			code = v.Code
		}
		// fmt.Println(code)
		log.Debug("FAILEDDEBUG", "/", code_key, "/", code, "/", v.Name, "/", u.Id)
		if errHincr := redisClient.HIncrBy(code_key, strconv.Itoa(code), 1).Err(); errHincr != nil {
			log.Error(errHincr)
		}
		if errExpire := redisClient.Expire(code_key, time.Duration(259200)*time.Second).Err(); errExpire != nil {
			log.Error(errExpire)
		}

	}
	return nil

}

func processURL(u Url) error {
	result := DDevices{}
	// log.Debug(u)
	query := func(c *mgo.Collection) error {
		fn := c.Find(bson.M{"_id": u.Dev_id}).One(&result)
		return fn
	}
	search := func() error {
		return withCollection("device", query)
	}

	err := search()
	if err != nil {
		log.Error(err)
		return err
	}
	var code int = 200
	dd, _ := time.ParseDuration("-1h")
	tt := time.Now()
	datestr := fmt.Sprint(tt.Add(dd).Format("20060102"))
	// fmt.Println(datestr)

	for _, v := range result.Deivces {
		code_key := fmt.Sprintf("%s_%s", datestr, v.Name)
		code = v.Code
		log.Debug("FINISHED", "/", code_key, "/", code, "/", v.Name, "/", u.Id)
		if errHincr := redisClient.HIncrBy(code_key, strconv.Itoa(code), 1).Err(); errHincr != nil {
			log.Error(errHincr)
		}
		if errExpire := redisClient.Expire(code_key, time.Duration(259200)*time.Second).Err(); errExpire != nil {
			log.Error(errExpire)
		}

	}
	return nil
}

func init() {
	testConfig := `
<seelog>
    <outputs formatid="main">

        <filter levels="trace,debug,info,warn,error,critical">
            <file path="/Application/refresh/logs/check.log"/>

        </filter>
    </outputs>

    <formats>
        <format id="main" format="%Date/%Time %File:%Line %FuncShort [%LEV] %Msg%n"/>
    </formats>
</seelog>
`
	// <filter levels="trace,info,debug,warn,critical,error">
	//     <console />
	// </filter>
	// <file path="/home/vance/work/Go/src/Ultron/logs/check.log"/>
	logger, _ := log.LoggerFromConfigAsBytes([]byte(testConfig))
	log.ReplaceLogger(logger)
	redisClient = redis.NewClient(&redis.Options{
		Addr:         redisHost,
		Password:     "bermuda_refresh",
		DB:           cacheDB,
		PoolSize:     10, //default is 10 connections
		PoolTimeout:  time.Duration(120) * time.Second,
		IdleTimeout:  time.Duration(240) * time.Second, //240s
		DialTimeout:  time.Duration(60) * time.Second,  //30s
		ReadTimeout:  time.Duration(60) * time.Second,  //10s
		WriteTimeout: time.Duration(60) * time.Second,  //10s
	})
	pong, err := redisClient.Ping().Result()
	fmt.Println(pong, err)
	if err != nil {
		// log.Debug("Connect to redis error", err)
		panic(err)
	}
}

func getSession() *mgo.Session {
	if session == nil {
		var err error
		session, err = mgo.DialWithTimeout(uri, 2*time.Minute)
		// session, err = mgo.Dial(uri)//timeout default 10* time.Second
		if err != nil {
			panic(err)
		}
	}
	// Optional. Switch the session to a monotonic behavior.
	session.SetMode(mgo.Monotonic, true)
	session.SetSocketTimeout(2 * time.Minute)
	//默认4096
	return session.Clone()
}

func withCollection(collection string, s func(*mgo.Collection) error) error {
	session := getSession()
	defer func() {
		session.Close()
		if err := recover(); err != nil {
			log.Debug(err)
		}
	}()
	c := session.DB(databaseName).C(collection)
	return s(c)
}

func main() {
	st := time.Now()
	log.Debug("start time:", st)
	defer log.Flush()

	urlList := getUrls()
	ll := len(urlList)
	log.Debug("count:", ll)
	var wg sync.WaitGroup
	// d := session.DB("bermuda").C("device")
	go func() {
		for _, u := range urlList {
			select {
			case taskChannel <- u:
				// log.Debug(u)
				wg.Add(1)
			default:
				log.Debug("CHANNEL is full")
			}

			// ll = ll - 1
		}
	}()

	ct := time.Now()
	log.Debug("start goroutine:", ct)
	for i := 0; i < goroutineNum; i++ {
		go func() {
			for {
				select {
				case task := <-taskChannel:
					log.Debug("get task:", task, task.RetryBranchID)
					if task.Status == "FINISHED" && !task.RetryBranchID.Valid() {
						processURL(task)
					} else {
						processFailedURL(task)
					}

					wg.Done()
					// default:
					// 	log.Debug("CHANNEL is Null")
				}
			}
		}()
	}
	wg.Wait()
	entime := time.Now()
	log.Debug("end time:", entime)
	log.Debug("use times:", entime.Sub(st).Seconds())

}
