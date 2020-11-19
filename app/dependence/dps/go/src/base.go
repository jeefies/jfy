package main

import "C"

type User interface {
	Email string
	Name string
	Password string
	Permission string
	Sex string
	Age string
	Birthday string
	Locale string
	Country string
	Description string
}


//export CACHE
CACHE map[string] *User := make(map[string] *User)

//export Init
func Init(list [][]string) {
	for (i:=0; i < len(list); i++) {
		u := list[i]
		NewUser(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9])
	}
}

//export NewUser
func NewUser(email, name, password, permission, sex, age, birthday, locale, country, description string) *User {
	user, ok := CACHE[email]
	if ok {
		return user
	} else {
		user = &User{email, name, password, permission, sex, age, birthday, locale, country, description}
		CACHE[email] = user
		CACHE[name] = user
		return user
	}
}

func (u *User) Get(ml_nm string) *User {
	user := CACHE[ml_nm]
	return user
}

func main() {
}
