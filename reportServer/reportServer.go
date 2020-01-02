package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/go-martini/martini"
	"github.com/vharitonsky/iniflags"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
)

var m *martini.Martini
var uri string = fmt.Sprintf("mongodb://bermuda:bermuda_refresh@%s:27017/bermuda", "223.202.52.135")
var rurl = flag.String("report_url", "http://223.202.52.83/receiveService", "send report to")
var port = flag.Int("port", 3000, "Port to listen to")
var retryCount = 3

type RequestBody struct {
	Status  string   `json:"status"`
	Region  []string `json:"region"`
	Percent string   `json:"percent"`
	Task_id string   `json:"task_id"`
}

type Message struct {
	Id          bson.ObjectId `bson:"_id"`
	Task_id     string        `bson:"task_id"`
	Body        RequestBody
	Create_time time.Time `bson:"create_time"`
	Post        string    `bson:"post"`
	Code        int       `bson:"code"`
	Reponse     string    `bson:"reponse"`
}

// DB Returns a martini.Handler
func DB() martini.Handler {
	session, err := mgo.Dial(uri)
	if err != nil {
		panic(err)
	}

	return func(c martini.Context) {
		s := session.Clone()
		c.Map(s.DB("bermuda"))
		defer s.Close()
		c.Next()
	}
}

// func init() {
// 	iniflags.OnFlagChange("conf.ini", func() {
// 		setServerConf(*conf.ini)
// 	})
// 	m = martini.New()
// 	m.Use(martini.Logger())
// 	m.Use(martini.Recovery())
// 	m.Use(DB())

// 	r := martini.NewRouter()
// 	r.Get('/report',TestReport)
// 	r.Post('/report',ProcessReport)

// 	m.Action(r.Handle())
// }
// func ReportList() {

// }

//
// Parse the request body, load into an Album structure.
func getPostMessage(r *http.Request, logger *log.Logger) *RequestBody {
	decoder := json.NewDecoder(r.Body)
	var rbody RequestBody
	err := decoder.Decode(&rbody)
	if err != nil {
		log.Println(err)

	}
	logger.Println(rbody)
	return &rbody

}

func saveMessage(body RequestBody, db *mgo.Database, logger *log.Logger, code int, rbody string, url string) error {
	// var msg Message
	// db := DB()
	collection := db.C("callback")
	//insert mongodb need +8
	tt := time.Now().Add(time.Hour * 8)
	logger.Println(body)
	doc := Message{Id: bson.NewObjectId(), Task_id: body.Task_id, Body: body, Create_time: tt, Post: url, Code: code, Reponse: rbody}
	err := collection.Insert(doc)
	if err != nil {
		logger.Printf("Can't insert document: %v\n", err)
		os.Exit(1)
	}
	return err
}

func sendMessage(rbody RequestBody, logger *log.Logger, db *mgo.Database) error {

	// Urls := []string{"http://cdnresource.duowan.com/lctq/client/js/platformAnalyse.js"}
	// purl := *rurl //"http://223.202.52.83/receiveService"
	purl := strings.Split(*rurl, ",")
	b, err := json.Marshal(rbody)
	if err != nil {
		logger.Println("json err:", err)
	}
	reCode := 0
	var reBody string = ""
	logger.Println(string(b))
	// body := bytes.NewBuffer([]byte(b))

	n, err := db.C("callback").Find(bson.M{"task_id": rbody.Task_id}).Count()
	if n > 0 {
		logger.Printf("%s is old", rbody.Task_id)
		return nil
	}

	for _, uu := range purl {
		for num := 0; num <= retryCount; num++ {
			// client := &http.Client{}
			// // resp, err := http.Post(uu, "application/json", body)
			body := bytes.NewBuffer([]byte(b))
			client := &http.Client{}
			// req, _ := http.NewRequest("POST", "http://223.202.52.83/receiveService", body)
			req, _ := http.NewRequest("POST", uu, body)

			req.Header.Set("Content-Type", "application/json") //这个一定要加，不加form的值post不过去，被坑了两小时
			// fmt.Printf("%+v\n", req)
			// req.Body = ioutil.NopCloser(body) //看下发送的结构

			resp, err := client.Do(req) //发送
			if err != nil {
				logger.Println(err)
				reCode = 500
				reBody = ""
				continue
			}

			defer resp.Body.Close() //一定要关闭resp.Body
			r_body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				logger.Println(err)
				reCode = 500
				// reBody = ""
				continue
			}
			reBody = string(r_body)
			reCode = resp.StatusCode
			if reCode == 200 {
				break
			}

		}
		logger.Println(reBody)
		err := saveMessage(rbody, db, logger, reCode, reBody, uu)
		if err != nil {
			logger.Println(err)
		}

	}

	return nil
}

func ProcessReport(w http.ResponseWriter, r *http.Request, db *mgo.Database, logger *log.Logger) (int, error) {
	body := getPostMessage(r, logger)
	logger.Println(body)
	var err error
	if body.Status == "SUCCESS" {
		err = sendMessage(*body, logger, db)

	}

	// err := saveMessage(*body, db, logger, code, rbody)

	return 200, err
}

func main() {
	m := martini.Classic()
	m.Use(martini.Logger())
	// m.Use(martini.Recovery())
	m.Use(DB())
	f, err := os.OpenFile("/Application/bermuda/logs/translog.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer f.Close()
	iniflags.Parse()
	m.Map(log.New(f, "[martini]", log.LstdFlags|log.Lshortfile))
	// m.MapTo(db, (*DB)(nil))

	// m.Get('/report',ReportList)
	m.Post("/report", ProcessReport)
	m.Get("/", func() string {
		return "Hello world!"
	})
	m.RunOnAddr(fmt.Sprintf(":%d", *port)) //
	// m.Run()
}
