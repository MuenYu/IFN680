package main

import (
	"github.com/tealeg/xlsx/v3"
	"log"
	"os"
	"strings"
	"sync"
	"time"
)

var (
	xlsxFile *xlsx.File  = nil
	sheet    *xlsx.Sheet = nil
	statsWg  sync.WaitGroup
)

// statistic record
type statsRecord struct {
	house     string
	error     string
	macro     string
	algorithm string
	*taskResult
}

func (sr statsRecord) write2Row() {
	tmp := strings.Split(sr.house, string(os.PathSeparator))

	row := sheet.AddRow()
	row.AddCell().SetString(tmp[len(tmp)-1])
	row.AddCell().SetString(sr.error)
	row.AddCell().SetString(sr.macro)
	row.AddCell().SetString(sr.algorithm)
	if sr.taskResult != nil {
		row.AddCell().SetFloat(sr.Duration)
		row.AddCell().SetString(sr.Solution)
	}
}

func openOrCreateXlsx() *xlsx.File {
	wb, err := xlsx.OpenFile(*outputFile)
	if err != nil {
		wb = xlsx.NewFile()
	}
	return wb
}

func newWorkSheet(xf *xlsx.File) *xlsx.Sheet {
	sh, err := xf.AddSheet(time.Now().Format("20060102150405"))
	if err != nil {
		log.Println(err.Error())
		os.Exit(1)
	}
	row := sh.AddRow()
	row.AddCell().SetString("house file")
	row.AddCell().SetString("error")
	row.AddCell().SetString("is macro")
	row.AddCell().SetString("search algorithm")
	row.AddCell().SetString("duration")
	row.AddCell().SetString("solution")
	return sh
}

func initStats() {
	xlsxFile = openOrCreateXlsx()
	sheet = newWorkSheet(xlsxFile)
}

func runStats(statsChan chan statsRecord) {
	for record := range statsChan {
		statsWg.Add(1)
		go func(record statsRecord) {
			defer statsWg.Done()
			record.write2Row()
		}(record)
	}
}

func outputReport(statsChan chan statsRecord) {
	statsWg.Wait()
	if err := xlsxFile.Save(*outputFile); err != nil {
		log.Println(err.Error())
	}
}
