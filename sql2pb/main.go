package main

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/Mikaelemmmm/sql2pb/core"
	_ "github.com/go-sql-driver/mysql"
)

func main() {

	dbType := "mysql"
	connStr := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s", "root", "root", "127.0.0.1", 3306, "test")
	pkg := "pb"
	goPkg := "./pb"
	table := "*"
	serviceName := "test"

	db, err := sql.Open(dbType, connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	s, err := core.GenerateSchema(db, table, nil, serviceName, goPkg, pkg)

	if nil != err {
		log.Fatal(err)
	}

	if nil != s {
		fmt.Println(s)
	}
}
