package main
import "C"
import "fmt"
import (
	"github.com/go-redis/redis"
	"strconv"
)

var client = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB: 0,
})

var key = "generateId"
var MAX int64 = 20
var start int64 = 0

func init()  {
	pong, err := client.Ping().Result()
	fmt.Println(pong, err)
	if err != nil {
		fmt.Println("Redis Connection Successful")
	}
}

func getUniqueId()  {
	uniqueId := client.LPop(key).Val()
	if uniqueId == "" {
		addToList(0)
		return
	}
	nextElem,_ := strconv.ParseInt(uniqueId, 10, 64)
	nextElem += 1
	nextElem = nextElem + MAX
	client.RPush(key,nextElem)
}

func addToList(start int64)  {
	for start <= MAX {
		client.RPush(key,start)
		start = start + 1
	}
}
//export run
func run()  {
	var index = client.LLen(key).Val() - 1
	elem := client.LIndex(key, index)
	if elem != nil {
		getUniqueId()
	} else {
		addToList(start)
	}
}

func main() {
//	for n := 0; n <= 20; n++ {
//		run()
//	}
}