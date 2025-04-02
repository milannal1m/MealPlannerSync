<script>

import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      router: useRouter(),
      username: "",
      error: null,
      response: null
    };
  },

  methods: {
    login() {
      if (this.username.trim()) {
        localStorage.setItem('user', this.username); // Benutzername speichern
              const url = new URL("http://" + window.location.hostname + "/user/users");
              url.searchParams.append("username", this.username);

              fetch(url, {
                method: "POST",
              })
                .then(response => response.json())
                .then(data => console.log("Erfolgreich erstellt:", data))
                .catch(error => {
                  console.error("Error:", error);
                });

              // Weiterleitung zur Hauptseite
              this.router.push('/home');
      } else {
        this.error = 'Bitte einen Benutzernamen eingeben';
      }
    },
  }
  };


</script>

<template>

  <div class="flex items-center justify-center h-screen bg-gray-100">

    <div class="bg-white p-6 rounded shadow-lg w-80">

      <h2 class="text-xl font-bold mb-4 text-center">Enter Username</h2>
      
      <input 
        v-model="username" 
        placeholder="Enter Username" 
        class="w-full p-2 border rounded mb-2" 
      />
      
      <p v-if="error" class="text-red-500 text-sm mb-2">{{ error }}</p>
      
      <button @click="login" class="w-full bg-blue-500 text-white p-2 rounded">
        Login
      </button>

    </div>

  </div>

</template>