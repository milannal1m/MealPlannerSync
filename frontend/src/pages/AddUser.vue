<script>

    import BackButtonUser from '@/components/BackButtonUser.vue';
                                                                                                                                                                                                                                                                                                                                                          
    export default {
      data() {
        return {
          username: sessionStorage.getItem('user'),
          name: "",
          error: null
        };
      },

      components: {
        BackButtonUser
      },

      methods: {
        addUser(name) {
          const url = new URL("http://localhost/user/users/" + this.username + "/connections"); 
          url.searchParams.append("connected_username", name);

          fetch(url, {
            method: "Post"
          })
          .then(response => response.json())
          .then(data => console.log("Erfolgreich erstellt:", data))
          .catch(error => {
            console.error("Error:", error);
          });
        }
      }
      
    };

</script>

<template>
    
  <div class="p-4 max-w-md mx-auto bg-white rounded shadow">
    <div class = "user-header">
      <BackButtonUser />
      <h1 class="text-xl font-bold mb-4">Add Connection</h1>
    </div>
    
    <div class = "form-group">
        <label class="meal-name">Username:</label>
        <input v-model="name" placeholder="Username" />
    </div>

    <button @click="addUser(name)" class="save-button">
      Save
    </button>

  </div>

</template>

<style>

    .user-header {
        display: flex;
        align-items: center;
        gap: 10px; /* Abstand zwischen den Elementen */
    }

    .form-group {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }

    .save-button {
        background: #ffc107;
        font-size: 14px; /* Größere Schrift */
        font-weight: bold;
        display: flex; /* Zentriert den Inhalt */
        align-items: center; /* Zentriert vertikal */
        justify-content: center; /* Zentriert horizontal */
        border: none; /* Entfernt den Standard-Rand */
        border-radius: 8px; /* Runde Ecken */
        cursor: pointer;
        padding: 12px 18px; /* Abstand */
    }

    .save-button:hover {
        background: #e0a800;
    }

</style>