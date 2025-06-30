#!/bin/bash
# Script de backup para MCP Licitações

DATA=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="backup_$DATA"

mkdir -p $BACKUP_DIR
cp -r src config data logs requirements.txt pyproject.toml $BACKUP_DIR/
echo "Backup realizado em $BACKUP_DIR" 