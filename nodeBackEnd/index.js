/*!
 * express
 * Copyright(c) 2009-2013 TJ Holowaychuk
 * Copyright(c) 2013 Roman Shtylman
 * Copyright(c) 2014-2015 Douglas Christopher Wilson
 * MIT Licensed
 */

'use strict';

module.exports = require('./lib/express');

const express = require('express')
const app = express()

var pgp = require('pg-promise')(/*options wut?*/)
//var db = pgp('postgres://nodetest:nodetest@localhost:5432/puppies')
var db = pgp('postgres://restbot:resty@172.17.0.2:5432/postgres')

/*app.get('/api/getPuppers', function (req, res, next) {
  db.any('select * from pups')
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved ALL puppies'
        });
    })
    .catch(function (err) {
      return next(err);
    });
})*/

app.get('/api/getAllSales', function (req, res, next) {
  db.any('SELECT * FROM appidtable')
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved ALL puppies'
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
          message: 'Retrieved ALL puppies'
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
          message: 'Retrieved ALL puppies'
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
          message: 'Retrieved ALL puppies'
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
  res.send("This is the api test!")
})

//POST
app.post('/', function (req, res) {
  res.send('Got a POST request')
})

//PUT
app.put('/user', function (req, res) {
  res.send('Got a PUT request at /user')
})

//DELETE
app.delete('/user', function (req, res) {
  res.send('Got a DELETE request at /user')
})


app.listen(3000, () => console.log('Example app listening on port 3000!'))
