/*!
 * express
 * Copyright(c) 2009-2013 TJ Holowaychuk
 * Copyright(c) 2013 Roman Shtylman
 * Copyright(c) 2014-2015 Douglas Christopher Wilson
 * MIT Licensed
 */

'use strict';

const express = require('express')
const app = express()

var pgp = require('pg-promise')(/*options wut?*/)
var db = pgp('postgres://restbot:resty@172.18.0.3:5432/postgres')

//trying to get over the Same Origin Policy bullshit using cross-origin resource sharing
//TODO: Don't use wildcards like a muppet
app.use(function(req, res, next) {
	res.setHeader("Access-Control-Allow-Origin", "*");
	res.setHeader("Access-Control-Allow-Headers","X-Requested-With,content-type");
	res.setHeader("Access-Control-Allow-Methods", "GET");
	res.setHeader("Access-Control-Allow-Credentials", true);
	next();
});

app.get('/api/getAllSales', function (req, res, next) {
  db.any('SELECT * FROM appidtable')
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved all games list'
        });
    })
    .catch(function (err) {
      return next(err);
    });
})
app.get('/api/get50OffSales', function (req, res, next) {
  db.any('SELECT * FROM appidtable WHERE discount >= 50')
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved 50% off games list'
        });
    })
    .catch(function (err) {
      return next(err);
    });
})
app.get('/api/get90OffSales', function (req, res, next) {
  db.any('SELECT * FROM appidtable WHERE discount >= 90')
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved 90% off games list'
        });
    })
    .catch(function (err) {
      return next(err);
    });
})
app.get('/api/game/*', function (req, res, next) {
  var id = req.params;
  db.any('SELECT * FROM appidtable WHERE appid = '+ id[0])
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved specific game'
        });
    })
    .catch(function (err) {
      return next(err);
    });
})
app.get('/api/percentageoff/*', function (req, res, next) {
  var id = req.params;
  db.any('SELECT * FROM appidtable WHERE discount >= '+ id[0])
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved specific game discount'
        });
    })
    .catch(function (err) {
      return next(err);
    });
})


//GET
app.get('/', function (req, res) {
  res.send('Hello World!')
})

app.get('/about', function (req, res) {
  res.send('This is an about page dude! :D')
})

app.get('/api/getData', function (req, res) {
  res.send("No data for you, you do not know the secret ways!")
})

app.listen(3000, () => console.log('Example app listening on port 3000!'))
