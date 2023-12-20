#!/bin/bash

source current_version.env
export CURRENT_VERSION

MODE="dev"
DB_HOST="localhost"
HOSTNAME="localhost"
OPENAI_API_KEY="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" ## ADD KEY HERE
LANGUAGE="english"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --host)
            HOSTNAME="$2"
            shift
            ;;
        --mode)
            MODE="$2"
            if [ "$MODE" == "prod" ]; then
                DB_HOST="chatbot-db"
            fi
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
echo "Using hostname: $HOSTNAME"
echo "Bot language: $LANGUAGE"

docker compose down

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
echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> ./backend/.env

## GPT4
echo "OPENAI_ENGINE=openai-azure-insait" >> ./backend/.env

## GPT3.5
# echo "OPENAI_ENGINE=gpt-35-turbo" >> ./backend/.env

echo "DB_HOST=$DB_HOST" >> ./backend/.env
echo "DB_PASSWORD=password" >> ./backend/.env
echo "DB_NAME=chatbot" >> ./backend/.env
echo "DB_PORT=5432" >> ./backend/.env
echo "DB_USERNAME=user" >> ./backend/.env
echo "LOG_TO_FILE_ENABLED=0" >> ./backend/.env
echo "LOGS_PATH=bot_logic/logs" >> ./backend/.env
echo "CURRENT_LANGUAGE=$LANGUAGE" >> ./backend/.env


if [ "$MODE" == "dev" ]; then
    docker compose build --no-cache chatbot-db
    docker compose up -d chatbot-db
else
    docker compose build --no-cache
    docker compose up -d
fi
