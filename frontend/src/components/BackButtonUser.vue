<script setup>

import { useRouter } from 'vue-router';

const router = useRouter();

const navigateBack = () => {
  router.push('/user'); 
};

</script>

<template>

  <button @click="navigateBack" class="back-button">
    Back
  </button>
  
</template>

<style>
  .back-button {
    background: #007bff; /* Blaue Farbe für Benutzer-Button */
    font-size: 18px; /* Größere Schrift */
    display: flex; /* Zentriert den Inhalt */
    align-items: center; /* Zentriert vertikal */
    justify-content: center; /* Zentriert horizontal */
    border: none; /* Entfernt den Standard-Rand */
    border-radius: 8px; /* Runde Ecken */
    cursor: pointer;
    padding: 12px 18px; /* Abstand */
    color: white; /* Weiße Schrift */
  }

.back-button:hover {
  background: #0056b3; /* Dunkleres Blau beim Hover */
}

</style>