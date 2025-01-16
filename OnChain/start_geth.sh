#!/bin/bash
geth --http --http.addr "0.0.0.0" --http.port 8545 --http.api "eth,net,web3" --networkid 11155111 --syncmode "snap"
