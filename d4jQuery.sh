#!/bin/bash
export PATH=$PATH:/home/gerardo/defects4j/framework/bin
defects4j query -p $2 -q "bug.id,revision.id.buggy,revision.id.fixed,report.id,report.url,revision.date.buggy,revision.date.fixed" -o $1
