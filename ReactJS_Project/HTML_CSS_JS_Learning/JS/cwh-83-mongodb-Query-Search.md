## Searching for data in mongo db

## Create Or Switch Database

```
use Prashant
```


## Insert Multiple Rows

```
db.items.insertMany([
  {
    "name":"Samsung 30s",
    "price":22000,
    "rating":4.5,
    "qty":233,
    "sold":98
  },
  {
    "name":"Moto 30s",
    "price":29000,
    "rating":3.5,
    "qty":133,
    "sold":598
  },
  {
    "name":"Realme 80s",
    "price":129000,
    "rating":2.5,
    "qty":633,
    "sold":98,
    "isBig":true
  }
])
```

## This query will return all the objects with rating equal to 3.5
```
db.items.find({rating: 3.5})
db.items.find({rating: {$gte: 3.5}})
db.items.find({rating: {$gt: 3.5}})
```

## And operator
```
db.items.find({rating: {$gt: 3.5}, price:{$gt: 4000}})
db.items.find({rating: {$lt: 3.5}, price:{$gt: 114000}})
```

## Or operator
```
db.items.find({$or:[{rating: {$lt: 3.5}}, {price:{$gt: 114000}}]})
db.items.find({$or:[{rating: {$gt: 3.5}}, {rating: 1}]})
```