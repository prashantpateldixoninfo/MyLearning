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
## Find the item with price 22000
```
db.items.find({price: 22000})
```


## Deleting items from the Mongo Database
```
db.items.deleteOne({price: 22000})
```

## deleteOne will delete the matching document entry and will delete the first entry in case of multi document match
```
db.items.deleteMany({price: 129000})
```