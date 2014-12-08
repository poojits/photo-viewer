var express = require('express');
var router = express.Router();
var fs = require('fs');
function getDir(dir) {
  var idx = dir.lastIndexOf('/');
  return dir.substr(idx+1, dir.length);
}
function findValInArray(json, key){
  console.log(json);
  for(var i=0; i<json.length;i++){
    if(json[i].hasOwnProperty(key)){
      return json[i][key];
    }
  }
}

var walk2json = function(paths) {
	var root = {};
  var files = [];
  for(var i=0;i<paths.length;i++){
    var slash = paths[i].indexOf('/');
    //console.log('slash=' + slash);
    if(slash > 0){
      var dir = paths[i].substr(0,slash);
      //console.log('dir='+dir);
      var sub = paths[i].substr(slash+1,paths[i].length);
      //console.log('sub='+sub);
      if(root.hasOwnProperty(dir)){
        root[dir].push(sub);
      }else{
        root[dir] = [];
        root[dir].push(sub);
      }
    }
    else{
      files.push(paths[i]);
    }
  }
  
  if(Object.keys(root).length==0){
    return files;
  }
  else{
    output = [];
    for(var i=0;i<Object.keys(root).length;i++){
      var key = Object.keys(root)[i];
      var value = root[key];
      var recurse = walk2json(value);
      obj[key] = recurse;
      output.push(obj);
    }
    return output;
  }
};
/* GET home page. */
router.get('/', function(req, res) {
  res.render('index', { title: 'CS576 - PhotoViewer' });
});

router.get('/cluster', function(req, res) {
    var dir = './public/' + req.query.directory;
    var repExists = false;
    fs.readdir(dir, function(err, list) {
      var files = [];
      var directory = []; 
      list.forEach(function(file) {
        file = dir + '/' + file;
        if(file.indexOf('rep.json')<0){
          if(file.indexOf('.DS_Store')<0){
            if(fs.lstatSync(file).isDirectory())
              directory.push(file.replace('./public/',''));
            else
              files.push(file.replace('./public/',''));
          }
        }
        else{
          repExists = true;
        }
      });
      var obj = {};
      var dirArray = [];
      if(repExists){
        var rep = JSON.parse(fs.readFileSync(dir+'/rep.json', "utf8"));
        for(var i=0;i<directory.length;i++){
          var dirobj = {};
          dirobj["name"] = directory[i];
          dirobj["rep"] = findValInArray(rep, getDir(directory[i]));
          dirArray.push(dirobj);
        }
      }
      obj["files"] = files;
      obj["directories"] = dirArray;
      res.json(obj);
    });
});

module.exports = router;
