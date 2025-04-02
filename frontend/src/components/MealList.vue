<script>

  export default {
    props: {
        searchQuery: {
        type: String,
        required: true
      }
    },

    data() {
      return {
        username: localStorage.getItem('user'),
        meals: [],
        error: null,
        filter: ""
      };
    },

    mounted() {
      fetch("http://" + window.location.hostname + "/sync/" + this.username + "/synced_meals")
        .then(response => response.json())
        .then(data => {
          this.meals = data; // Speichert die Daten in der Variable
          console.log(this.meals)
        })
      .catch(error => {
        console.error("Error:", error);
        this.error = error; // Speichert den Fehler, falls nötig
      });

      const meal_socket = new WebSocket("http://" + window.location.hostname + "/meal/ws");

      meal_socket.onopen = function() {
        console.log("WebSocket ist verbunden.");
      };

      meal_socket.onmessage = function(event) {
        console.log("Nachricht vom Server:", event.data);

        location.reload();
      };

      const user_socket = new WebSocket("http://" + window.location.hostname + "/user/ws");

          user_socket.onopen = function() {
            console.log("WebSocket ist verbunden.");
          };

          user_socket.onmessage = function(event) {
            console.log("Nachricht vom Server:", event.data);
            
            location.reload();
          };
    },

    methods: {
      deleteMeal(index, owner) {
        if(owner == this.username) {
        fetch("http://" + window.location.hostname + "/meal/" + this.username + "/meals/" + index, {
          method: "DELETE"
        })
          .then(response => {
          if (!response.ok) {
            throw new Error("Fehler beim Löschen");
          }
          console.log("Meal gelöscht");
        })
        .catch(error => console.error("Fehler:", error));
      }
      else 
        alert("You are not the owner of this meal and cannot delete it.");
      },
      
      editItem(meal) {
        this.$router.push({
          path: '/meal',
          query: meal
        })
      }
    }
      
  };


</script>

<template>
  <ul class="meal-list">
    <li class = "meal-item"
      v-for="meal in this.meals.filter(meal => 
      meal.name.toLowerCase().includes(searchQuery.toLocaleLowerCase()) || 
      meal.owner.toLowerCase().includes(searchQuery.toLocaleLowerCase()) 
    )" 
      :key="meal.id">

      <div class="meal-info">
        <span class="meal-name">{{ meal.name }}  {{ meal.planned_for.split("T")[0]}}</span>
        <span class="meal-user">{{ meal.owner }}</span>
      </div>

      <div class="action-buttons">
      <button class="edit-button"
      @click = "editItem(meal)"><i class="fa-solid fa-arrow-right"></i></button>
      <button class="delete-button"
      @click="deleteMeal(meal.id, meal.owner)"><i class="fa-solid fa-trash"></i></button> 
      </div>

    </li>
  </ul>

</template>

<style>

  .meal-list {
    list-style: none;
    padding: 0;
  }

  .meal-item {
    background: #ffffff;
    padding: 12px;
    margin: 10px 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .meal-info {
    display: flex;
    flex-direction: column;
  }

  .meal-name {
    font-size: 18px;
    font-weight: bold;
  }

  .meal-user {
    font-size: 14px;
    color: #666;
  }

  .edit-button,
  .delete-button {
    width: 100px;  /* Feste Breite */
    height: 50px; /* Feste Höhe */
    font-size: 24px; /* Größere Schrift */
    display: flex; /* Zentriert den Inhalt */
    align-items: center;
    justify-content: center;
    border: none; /* Entfernt den Standard-Rand */
    border-radius: 8px; /* Runde Ecken */
    cursor: pointer;
    gap: 25px;
    margin-bottom: 10px; /* Vertikaler Abstand zwischen den Buttons */
  }

  .edit-button {
  background: #ffc107;
  }

  .edit-button:hover {
  background: #e0a800;
  }

  .delete-button {
  background: #dc3545;
  }

  .delete-button:hover {
  background: #c82333;
  }

</style>