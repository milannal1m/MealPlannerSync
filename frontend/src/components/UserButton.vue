<script setup>

  import { useRouter } from 'vue-router';
  import { defineProps } from 'vue';

  const props = defineProps({
    items: Array
  })

  const router = useRouter();

  const navigateToUser = () => {
    router.push({
      path: '/user',
      query: { items: JSON.stringify(props.items) }
    }); 
  };

</script>

<template>

    <button @click="navigateToUser" class="user-button">
      👤
    </button>
    
</template>

<style>
    .user-button {
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

.user-button:hover {
  background: #0056b3; /* Dunkleres Blau beim Hover */
}

</style>