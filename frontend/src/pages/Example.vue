
<-- GET -->

fetch("http://localhost/meal/test/meals")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Error:", error));


<-- POST -->

const url = new URL("http://localhost/meal/test/meals");
url.searchParams.append("name", "Pizza");
url.searchParams.append("date", "2025-03-30T12:00:00");

fetch(url, {
  method: "POST"
})
  .then(response => response.json())
  .then(data => console.log("Erfolgreich erstellt:", data))
  .catch(error => console.error("Fehler:", error));



<-- DELETE -->

fetch("http://localhost/meal/test/meals/6", {
  method: "DELETE"
})
  .then(response => {
    if (!response.ok) {
      throw new Error("Fehler beim Löschen");
    }
    console.log("Meal gelöscht");
  })
  .catch(error => console.error("Fehler:", error));


<-- Web Sockets -->

const socket = new WebSocket("http://localhost/meal/ws");

socket.onmessage = function(event) {
    console.log("Nachricht vom Server:", event.data);
};