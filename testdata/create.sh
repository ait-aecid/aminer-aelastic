#!/bin/bash

curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/aminertest/data/1' -d '{"name": "james bond"}'

curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/aminertest/data/2' -d '{"name": "bruce wayne"}'

curl -XGET 'http://localhost:9200/aminertest/data/_search?pretty=true'
