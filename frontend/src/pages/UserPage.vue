<script>

  import BackButton from '@/components/BackButton.vue'; 
  import AddButtonUser from '@/components/AddButtonUser.vue';

  export default {

    data() {
      return {
        username: sessionStorage.getItem('user'),
        users: [],
        refresh: false,
        error: null 
      };
    },

    mounted() {
      fetch("http://" + window.location.hostname + "/user/users/" + this.username + "/connections")
        .then(response => response.json())
        .then(data => {
          this.users = data; // Speichert die Daten in der Variable
          console.log(this.users)
        })
      .catch(error => {
        console.error("Error:", error);
        this.error = error; // Speichert den Fehler, falls nötig
      });

      const user_socket = new WebSocket("http://" + window.location.hostname + "/user/ws");

      user_socket.onopen = function() {
        console.log("WebSocket ist verbunden.");
      };

      user_socket.onmessage = function(event) {
        console.log("Nachricht vom Server:", event.data);
        
        location.reload();
      };
    },

    components: {
      BackButton,
      AddButtonUser
    },

    methods: {
      deleteUser(name) {
        fetch("http://localhost/user/users/" + this.username + "/connections/" + name, {
          method: "DELETE"
        })
          .then(response => {
          if (!response.ok) {
            throw new Error("Fehler beim Löschen");
          }
          console.log("User gelöscht");
        })
        .catch(error => console.error("Fehler:", error));
      }
    }

  };
  
</script>

<template>
  <div class = "user-header">
    <BackButton />
    <h1>Connections</h1>
    <AddButtonUser />
  </div>

  <ul class = "user-list">
    <li v-for="user in this.users" 
      :key="user.id">

        <div class = "user-item user-name">{{ user.name }} 
          <button class="delete-button"
          @click = "deleteUser(user.name)"><i class="fa-solid fa-trash"></i></button> 
        </div>

      </li>
  </ul>

</template>

<style>

  .user-header {
    display: flex;
    align-items: center;
    gap: 10px; /* Abstand zwischen den Elementen */
  }

  .user-list {
    list-style: none;
    padding: 0;
  }

  .user-item {
    background: #ffffff;
    padding: 12px;
    margin: 8px 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 60%; /* Oder eine andere feste Breite, z. B. 400px */

    display: flex;
    justify-content: space-between; /* Hält Username links & Buttons rechts */
    align-items: center; /* Sorgt für gleiche Höhe */
  }

  .user-name {
    font-size: 20px;
    font-weight: bold	;
  }

  .delete-button {
  background: #dc3545;
  }

  .delete-button:hover {
  background: #c82333;
  }

</style>