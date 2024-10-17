package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path"
	"path/filepath"
	"runtime"
	"sync"
	"time"
)

var (
	// How many cpu cores
	numCPU = runtime.NumCPU()
	// CLI Parameters
	warehouseFolder = flag.String("folder", "./warehouses", "Specify the warehouse folder")
	macro           = flag.String("macro", "true", "true: use macro move, false: use elementary move")
	taboo           = flag.String("taboo", "false", "true: allow taboo move, false: no taboo move allowed")
	script          = flag.String("script", "./runner.py", "Specify the test script")
	algorithm       = flag.String("algorithm", "astar", "algorithm for sokoban solver, it should be astar or bfs")
	timeout         = flag.Duration("timeout", 3*time.Minute, "Specify the timeout for each task")
	outputFile      = flag.String("output", "./result.xlsx", "Specify the output .xlsx file to store result")
	concurrency     = flag.Int("concurrency", numCPU, "Specify the number of concurrent tests")
)

func loadWarehouse(folder string) []string {
	files, err := os.ReadDir(folder)
	if err != nil {
		log.Fatalln(fmt.Errorf("load warehouse folder failed: %v", err))
	}
	fileNames := make([]string, 0, len(files))
	for _, file := range files {
		if !file.IsDir() {
			absPath, err := filepath.Abs(path.Join(folder, file.Name()))
			if err != nil {
				log.Fatalln(fmt.Errorf("load warehouse folder failed: %v", err))
			}
			fileNames = append(fileNames, absPath)
		}
	}
	return fileNames
}

func main() {
	flag.Parse()
	houses := loadWarehouse(*warehouseFolder)

	wg := new(sync.WaitGroup)
	wg.Add(len(houses))
	stuckChan := make(chan struct{}, *concurrency)
	statsChan := make(chan statsRecord, len(houses))

	initStats()
	for _, house := range houses {
		go func(house string) {
			defer wg.Done()
			stuckChan <- struct{}{}
			record := runTask(house)
			statsChan <- record
			<-stuckChan
		}(house)
	}
	go func() {
		wg.Wait()
		close(stuckChan)
		close(statsChan)
	}()
	for record := range statsChan {
		record.write2Row()
	}
	if err := xlsxFile.Save(*outputFile); err != nil {
		log.Println(err.Error())
	}
}
