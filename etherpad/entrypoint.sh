echo "${ETHERPAD_API_KEY}" > APIKEY.txt
echo "API KEY created. Starting etherpad server..."
node src/node/server.js