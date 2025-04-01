
<-- GET -->

fetch("http://" + window.location.hostname + "/meal/test/meals")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Error:", error));


<-- POST -->

const url = new URL("http://" + window.location.hostname + "/meal/test/meals");
url.searchParams.append("name", "Pizza");
url.searchParams.append("date", "2025-03-30T12:00:00");

fetch(url, {
  method: "POST"
})
  .then(response => response.json())
  .then(data => console.log("Erfolgreich erstellt:", data))
  .catch(error => console.error("Fehler:", error));



<-- DELETE -->

fetch("http://" + window.location.hostname + "/meal/test/meals/6", {
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

const meal_socket = new WebSocket("http://" + window.location.hostname + "/meal/ws");

meal_socket.onmessage = function(event) {
    console.log("Nachricht vom Server:", event.data);
    // Hier refreshen wir die Liste der Meals
};

const user_socket = new WebSocket("http://" + window.location.hostname + "/user/ws");

user_socket.onmessage = function(event) {
    console.log("Nachricht vom Server:", event.data);
    // Hier refreshen wir die Liste der Meals
};