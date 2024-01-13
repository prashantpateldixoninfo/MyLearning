/* Create a business name generator by combining list of adjectives and shop name and another word


Adjectives:
Crazy 
Amazing
Fire 

Shop Name:
Engine
Foods
Garments

Another Word:
Bros
Limited
Hub



*/

let adjectives = ["Crazy", "Amazing", "Fire"];
let shopName = ["Engine", "Foods", "Garments"];
let anotherWord = ["Bros", "Limited", "Hub"];

let businessName = adjectives[Math.floor(Math.random() * 100) % 3] + " " + shopName[Math.floor(Math.random() * 100) % 3] + " " + anotherWord[Math.floor(Math.random() * 100) % 3];
console.log(businessName);
