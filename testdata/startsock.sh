#!/bin/bash

rm /tmp/test; ncat -nvl -U /tmp/test | jq
