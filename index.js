const http = require("http"); 
const express = require("express");
const app = express();
const path = require("path");
const bodyParser = require("body-parser");
const spawn = require('child_process').spawn;
var config = require('./config.json');

router = express.Router();


function getTimestampInSeconds () {
    return Math.floor(Date.now() / 1000).toString();
  }

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/public/getinfo.html'))
});


app.get('/submit', function(req, res){
    var FOLDER_NAME = getTimestampInSeconds();
    var uniqueID = req.query['uniqueID'];
    var depth = parseInt(req.query['depth']);
    var requestCount = parseInt(req.query['requestCount']);
    var worker = spawn(config.PythonPath, ['main.py', uniqueID, FOLDER_NAME, depth, requestCount]);
    worker.stdout.on('data', (data) => {
        console.log(`${data}`)
    });
    worker.on('exit', function() {
        res.download(path.join(__dirname, `${FOLDER_NAME}_archived.zip`));
    })
    
});

app.listen(8081);