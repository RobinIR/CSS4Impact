@echo off
REM Get the latest changes from Git
cd /d C:\CSS4Impact\Scrappers\css4impact
git pull

REM Get the latest changes from Git
cd /d C:\CSS4Impact\Database\css4impact
git pull

REM Start the database using Docker Compose
cd /d C:\CSS4Impact\Database\css4impact
docker-compose up -d

REM Get the latest changes from Git
cd /d C:\CSS4Impact\Website\css4impactfrontend
git pull

REM Start the frontend React project
cd /d C:\CSS4Impact\Website\css4impactfrontend
start cmd /k "npm install && npm run dev"

REM Wait for 5 seconds
ping 127.0.0.1 -n 15 > nul

REM Open the React project in the browser
start http://localhost:3000
