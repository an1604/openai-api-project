#!/bin/bash

# Load version configuration
source current_version.env
export CURRENT_VERSION

HOSTNAME="localhost"
DB_HOST="chatbot-db"
OPENAI_API_KEY="" ## ADD KEY HERE
LANGUAGE="english"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --host)
            HOSTNAME="$2"
            shift

            ;;
        *)
            echo "Unknown parameter passed: $1"
            exit 1
            ;;
    esac
    shift
done

echo "Current version: $CURRENT_VERSION"
echo "Bot language: $LANGUAGE"
echo "Using hostname: $HOSTNAME"

docker compose -f docker-compose-prod.yml pull 
docker compose -f docker-compose-prod.yml down

echo "VITE_BACKEND_URL=http://$HOSTNAME:5000" > ./frontend/.env
echo "VITE_CURRENT_LANGUAGE=$LANGUAGE" >> ./frontend/.env

# open_ai API
# echo "OPENAI_API_TYPE=open_ai" > ./backend/.env
# echo "OPENAI_API_VERSION=2020-11-07" >> ./backend/.env
# echo "OPENAI_API_BASE=https://api.openai.com/v1" >> ./backend/.env

# Azure API
echo "OPENAI_API_TYPE=azure" > ./backend/.env
echo "OPENAI_API_VERSION=2023-08-01-preview" >> ./backend/.env
echo "OPENAI_API_BASE=https://openai-azure-insait.openai.azure.com/" >> ./backend/.env

## GPT4
# echo "OPENAI_ENGINE=openai-azure-insait" >> ./backend/.env

## GPT3.5
echo "OPENAI_ENGINE=gpt-35-turbo" >> ./backend/.env

echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> ./backend/.env
echo "DB_HOST=$DB_HOST" >> ./backend/.env
echo "DB_PASSWORD=password" >> ./backend/.env
echo "DB_NAME=chatbot" >> ./backend/.env
echo "DB_PORT=5432" >> ./backend/.env
echo "DB_USERNAME=user" >> ./backend/.env
echo "LOG_TO_FILE_ENABLED=0" >> ./backend/.env
echo "LOGS_PATH=bot_logic/logs" >> ./backend/.env
echo "CURRENT_LANGUAGE=$LANGUAGE" >> ./backend/.env

docker compose -f docker-compose-prod.yml up -d
