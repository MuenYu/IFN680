package main

import (
	"context"
	"encoding/json"
	"errors"
	"log"
	"os"
	"os/exec"
)

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
