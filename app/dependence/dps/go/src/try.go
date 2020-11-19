package main

import "fmt"

type MyInt struct {
	Num int
}
func (mi *MyInt) Set(val int) {
	mi.Num = val
}

func main() {
	ca := make(map[string] *MyInt)
	var i int
	i = 1
	a := &MyInt{i}
	ca["a"] = a
	mi := ca["a"]
	mi.Set(2)
	fmt.Println(mi.Num)
	m1 := ca["a"]
	fmt.Println(m1.Num)
}
