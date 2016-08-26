var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
// var spawn = require('child_process').spawn;

child = require('child_process');

var modulesDirectory = __dirname + "/../modules/"

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});


router.get('/create', function(req, res, next) {

  var text = req.query.text
  
  var plaque_length = ""
  var plaque_width = ""
  var plaque_height = ""

  var col_space = ""
  var row_space = ""

  var x_space = ""
  var y_space = ""

  var dot_diameter = ""

  var cmd = 'python3 ' + modulesDirectory + 'braille/stlGenerator.py --text "' + text + '"';
  console.log(cmd)
  exec(cmd, {encoding: 'base64', maxBuffer: 5000 * 1024}, function(error, stdout, stderr) {
    if (error) {
      console.log(stderr);
      res.status(500).send();
    }
    else {
      res.send(stdout);
    }
  });
  
  // var braille_converter = spawn("python3", [modulesDirectory + 'braille/stlGenerator.py', '--text', '"' + text + '"'])

  // var payload = null;
  // var error = false;

  // braille_converter.stdout.on('data', function (data) {
  //   payload = new Buffer(data, 'ascii');
  // });

  // braille_converter.stderr.on('data', function (data) {
  //   console.log("ERROR: " + data);
  //   error = true;
  // });

  // braille_converter.on('close', function (code) {
  //   error ? res.status(500).send() : res.send(payload);
  // });

});

module.exports = router;
