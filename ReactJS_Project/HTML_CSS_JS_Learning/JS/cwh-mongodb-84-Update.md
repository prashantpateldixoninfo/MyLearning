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

## Update the Row
```
db.items.find()
db.items.updateOne({name: "Moto 30s"}, {$set: {price: 2}})
db.items.find()
db.items.updateMany({name: "Moto 30s"}, {$set: {price: 3, rating: 1}})
```