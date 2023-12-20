Chatbot App Production Deployment
This guide will walk you through deploying the Chatbot App using Docker and Docker Compose.

Table of Contents
Prerequisites
Installation of Docker and Docker Compose
Selecting a Host
Running the Deployment Script
Embedding the App

Prerequisites
A computer or server with macOS, Windows, or a UNIX-based system.
Terminal (for macOS or UNIX-based system) or Command Prompt/Powershell (for Windows) access.
Basic understanding of command-line operations.

Installation of Docker and Docker Compose
Docker: Download and install Docker suitable for your OS.

Docker Compose: Docker Compose is included in Docker Desktop for Windows and macOS. For Linux users, follow the official installation guide.

After installation, you can verify both installations with:

bash
Copy code
docker --version
docker-compose --version

Selecting a Host
By default, the app will run on localhost. If you're deploying on a remote server, you'll use the server's IP address or domain name as the host.

Running the Deployment Script
Navigate to the directory containing docker-compose-prod.yml and the deployment script:

bash
Copy code
cd /path/to/your/directory
Ask an admin for the azure OPENAI_API_KEY and add it in line 10 of the ./setup_and_run_prod.sh script
If you wish to specify a host other than localhost, run the script with the --host flag:

bash
Copy code
./your-script-name.sh --host=YOUR_HOST_NAME_OR_IP
Replace YOUR_HOST_NAME_OR_IP with your desired hostname or IP. If you don't specify a host, it defaults to localhost.

Embedding the App
iFrame:
Once your application is up and running, you can embed the app in an HTML page using:

html
Copy code

<iframe src="http://YOUR_HOST_NAME_OR_IP" width="100%" height="100%"></iframe>
Replace YOUR_HOST_NAME_OR_IP with your server's IP address or domain name.

React Native WebView:
To embed the application in a React Native app, you can use the react-native-webview package. If not already added, install it:

bash
Copy code
npm install react-native-webview
Then, in your React Native code:

jsx
Copy code
import WebView from 'react-native-webview';

function YourComponent() {
return (
<WebView source={{ uri: 'http://YOUR_HOST_NAME_OR_IP' }} style={{ flex: 1 }} />
);
}
Replace YOUR_HOST_NAME_OR_IP with your server's IP address or domain name.
