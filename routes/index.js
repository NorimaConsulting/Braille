var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;

child = require('child_process');

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
  var dot_stl_path = './DefaultMeshes/dot.stl'
  var plaque_stl_path= './DefaultMeshes/plaque.stl'



  var cmd = 'python ~/builder/builder.py ';
    exec(cmd, {encoding: 'binary', maxBuffer: 5000*1024}, function(error, stdout) {
      res.send(new Buffer(stdout, 'binary'));
    });

});

module.exports = router;
