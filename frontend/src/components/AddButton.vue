<script setup>

    import { useRouter } from 'vue-router';

    const router = useRouter();

    const navigateToMeal = () => {
        router.push(
            {
                path: '/meal'
            }
        );
    };

</script>

<template>

    <button @click="navigateToMeal" class="add-button">+</button>
    
</template>

<style>

.add-button {
        background: #28a745;
        font-size: 18px; /* Größere Schrift */
        display: flex; /* Zentriert den Inhalt */
        align-items: end;
        justify-content: end;
        border: none; /* Entfernt den Standard-Rand */
        border-radius: 8px; /* Runde Ecken */
        cursor: pointer;
        padding: 12px 18px;
        color: white;
  }

  .add-button:hover {
    background: #218838;
  }

</style>