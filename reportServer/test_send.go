package main1

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func main() {
	// v := url.Values{}
	// v.Set("huifu", "hello world")
	// body := ioutil.NopCloser(strings.NewReader(v.Encode())) //把form数据编下码
	client := &http.Client{}
	// req, _ := http.NewRequest("POST", "http://223.202.52.83/receiveService", body)
	req, _ := http.NewRequest("POST", "http://192.168.7.24:8080/examples/servlets/mh", strings.NewReader("namecjb"))

	req.Header.Set("Content-Type", "application/x-www-form-urlencoded; param=value") //这个一定要加，不加form的值post不过去，被坑了两小时
	fmt.Printf("%+v\n", req)
	// req.Body = ioutil.NopCloser(body) //看下发送的结构

	resp, err := client.Do(req) //发送
	defer resp.Body.Close()     //一定要关闭resp.Body
	data, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(data), err)
}
