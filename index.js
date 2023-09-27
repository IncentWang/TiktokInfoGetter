const http = require("http"); 
const express = require("express");
const app = express();
const path = require("path");
const bodyParser = require("body-parser");
const spawn = require('child_process').spawn;

router = express.Router();

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/public/getinfo.html'))
});

app.get('/submit', function(req, res){
    var url = req.query['firstURL'];
    var depth = parseInt(req.query['depth']);
    var requestCount = parseInt(req.query['requestCount']);
    var worker = spawn('C:/Users/18624/anaconda3/envs/tiktok/python.exe', ['main.py', url, depth, requestCount]);
    worker.stdout.on('data', (data) => {
        console.log(`${data}`)
    });
    
});

app.listen(8081);