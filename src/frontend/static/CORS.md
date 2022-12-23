# Cross origin resource sharing

Useful github discussion: <a href="https://github.com/tiangolo/fastapi/issues/1663"> link </a>

## What is CORS


**Cross origin resource sharing** is a system, consisting of transmitting HTTP headers, that determines whether browsers block frontend JavaScript code from accessing responses for cross-origin requests.

Cross-origin happens when the site and the APIs have different domains.

Source: <a href="https://stackoverflow.com/questions/20035101/why-does-my-javascript-code-receive-a-no-access-control-allow-origin-header-i" > link</a>

If you do not use a simple CORS request, usually the browser automatically also sends an OPTIONS request before sending the main request - more information is <a href = "https://stackoverflow.com/questions/10093053/access-control-request-headers-is-added-to-header-in-ajax-request-with-jquery/55584963#55584963"> here </a>. This is called a **preflight** request.

During the **preflight** request, you should see the following two headers: Access-Control-Request-Method and Access-Control-Request-Headers. These request headers are asking the server for permissions to make the actual request. Your preflight response needs to acknowledge these headers in order for the actual request to work.

## Example preflight request

Source: <a href="https://stackoverflow.com/questions/8685678/cors-how-do-preflight-an-httprequest"> link </a>

For example, suppose the browser makes a request with the following headers:

Origin: http://yourdomain.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: X-Custom-Header
Your server should then respond with the following headers:

Access-Control-Allow-Origin: http://yourdomain.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: X-Custom-Header


## Avoid preflight request

Source: <a href="https://developer.mozilla.org/en-US/docs/Glossary/CORS-safelisted_request_header"> link </a>

In order to avoid preflight request we can use all of the  <a href="https://fetch.spec.whatwg.org/#cors-safelisted-request-header"> **CORS-safelisted request header** </a>.
They are:

<li>Accept,
<li>Accept-Language,
<li>Content-Language,
<li>Content-Type.

<br>

    headers: new Headers({
      // Content-Type may need to be completely **omitted**
      // or you may need something
      'Accept': 'application/json',
      'Accept-Language': 'it',
      'Content-Language': 'it',
      'Content-Type': 'multipart/form-data'
    }),

When containing only these headers (and values that meet the additional requirements laid out below), a request doesn't need to send a preflight request in the context of CORS.

You can safelist more headers using the Access-Control-Allow-Headers header and also list the above headers.

Image from this <a href="https://stackoverflow.com/questions/10093053/access-control-request-headers-is-added-to-header-in-ajax-request-with-jquery/55584963#55584963"> discussion </a>.

![Alt text](https://i.stack.imgur.com/BTFel.png)



## Working solution

La soluzione ottenuta è descritta di seguito:

<li> Specifica dei metodi 'PUT', 'GET', 'POST', 'OPTIONS' all'interno della variabile allow_methods del CORSMiddleware all'interno di src/api/server.py. Il metodo **OPTIONS** è di fondamentale importanza per le PREFLIGHT requests effettuate dai browser.


<br>


<li> Il valore dell'header "Origin" nella richiesta del frontend al backend deve essere dentro gli allow_origins del CORSMidlleware del server di FastAPI (src/api/server.py). In questo caso l'Origin delle richieste è http://archinet-se4ai.ddns.net:9200; questo indirizzo è stato opportunamente aggiunto dentro gli allow_origins. Se una richiesta HTTP non va a buon fine bisogna verificare da console (voce 'Network->Headers') che il valore dell'header Origin all'interno della Request sia contenuta negli allow_origins di cui sopra.

<br>

<li> Utilizzo del dominio http://archinet-se4ai.ddns.net:9100 al posto di http://0.0.0.0:9100 nelle richieste effettuate dai file JS del frontend. L'utilizzo di localhost determinava il fallimento delle richieste

<br>

<li> Utilizzo di POSTMAN per il testing delle richieste a http://archinet-se4ai.ddns.net:9100 e, nel caso di risposta positiva dal server, generazione del codice Javascript-Jquery (Ajax) con l'opportuna funzione di POSTMAN.

<br>


**NB:** Per testare in locale sostituire gli indirizzi http://archinet-se4ai.ddns.net:9100 con http://0.0.0.0:9100 all'interno dei file javascript e testare con POSTMAN su http://0.0.0.0:9100 stesso.


