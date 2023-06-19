// 1. Variables: We can store information in variables.

var name = "John"; // this is a string
let age = 25; // this is a number
const isStudent = true; // this is a boolean

// 2. Functions: A block of code designed to perform a particular task. 

function greet(name) {
  console.log("Hello, " + name);
}

// Call the function
greet(name); // Outputs: "Hello, John"

// 3. Objects: JavaScript objects are containers for named values.

let student = {
  name: "John",
  age: 25,
  isStudent: true
};

// Access object properties
console.log(student.name); // Outputs: "John"

// 4. Arrays: A special type of object used for storing multiple values in a single variable.

let array = ["Apple", "Banana", "Cherry"];
console.log(array[0]); // Outputs: "Apple"

// 5. Loops: JavaScript supports different kinds of loops.

// This is a for loop
for (let i = 0; i < array.length; i++) {
  console.log(array[i]); // Outputs each fruit in the array
}

// 6. Conditional Statements: Used to perform different actions based on different conditions.

if (age >= 18) {
  console.log("You are an adult."); // Outputs: "You are an adult."
} else {
  console.log("You are a minor.");
}

// 7. Events: JavaScript's interaction with HTML is handled through events.

document.getElementById("myButton").onclick = function() { 
  alert('Hello World!'); 
};

// This will alert "Hello World!" when the element with id "myButton" is clicked.
