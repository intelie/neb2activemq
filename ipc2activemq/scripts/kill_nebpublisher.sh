#! /bin/bash
for pid in `ps aux | grep "python nebpublisher" | grep -v grep | awk '{print $2}'`; do sudo kill -9 $pid; done
