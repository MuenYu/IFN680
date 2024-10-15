package main

import (
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
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
	stuckChan := make(chan struct{}, numCPU)
	statsChan := make(chan statsRecord, len(houses))

	initStats()
	go runStats(statsChan)
	for _, house := range houses {
		wg.Add(1)
		go func(house string) {
			defer wg.Done()
			stuckChan <- struct{}{}
			record := runTask(house)
			statsChan <- record
			<-stuckChan
		}(house)
	}
	wg.Wait()
	outputReport(statsChan)
	close(stuckChan)
	close(statsChan)
}

func runTask(housePath string) statsRecord {
	ctx, cancel := context.WithTimeout(context.Background(), *timeout)
	defer cancel()

	record := statsRecord{
		house:     housePath,
		macro:     *macro,
		algorithm: *algorithm,
	}

	cmd := exec.CommandContext(ctx, "python", *script, "--macro", *macro, "--taboo", *taboo, "--house", housePath, "--algorithm", *algorithm)
	output, err := cmd.CombinedOutput()
	if err != nil {
		if errors.Is(ctx.Err(), context.DeadlineExceeded) {
			log.Println(housePath, ": timeout")
			record.error = "timeout"
		} else {
			log.Println(housePath, ":", err.Error())
			record.error = err.Error()
		}
		return record
	}
	log.Println(housePath, ": success")
	var result = &taskResult{}
	if err = json.Unmarshal(output, result); err != nil {
		log.Println(housePath, ":", err.Error())
		os.Exit(1)
	}
	record.taskResult = result
	return record
}

type taskResult struct {
	Duration float64 `json:"duration"`
	Solution string  `json:"solution"`
}
