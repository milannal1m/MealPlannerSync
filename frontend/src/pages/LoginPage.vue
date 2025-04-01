<script setup>

import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const error = ref('');

const login = () => {
  if (username.value.trim()) {
    sessionStorage.setItem('user', username.value); // Benutzername speichern
    router.push('/home'); // Weiterleitung zur Hauptseite
  } else {
    error.value = 'Bitte einen Benutzernamen eingeben';
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