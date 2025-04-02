<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import SearchBar from '../components/SearchBar.vue';
import MealList from '../components/MealList.vue';
import AddButton from '../components/AddButton.vue';
import UserButton from '../components/UserButton.vue';

const searchQuery = ref('');

const router = useRouter();

const editItem = (meal) => {
  router.push({
    path: '/meal',
    query: meal
  })
};

const logOut = () => {
  localStorage.removeItem('user');
  router.push({ path: '/' });
};

</script>

<template>
  <div class="user-header">
    <h1>Meal Planner</h1>
    <button class="logOut-button" @click="logOut"><i class="fa-solid fa-right-from-bracket"></i></button>
  </div>

  <div class="button-searchbar">
    <UserButton />
    <SearchBar v-model="searchQuery" />
    <AddButton />
  </div>
    <MealList :searchQuery="searchQuery" @editItem="editItem"/>
</template>

<style>

  .button-searchbar {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px; /* Abstand zwischen den Elementen */
    width: 100%;
  }

  .logOut-button {
    width: 80px;  /* Feste Breite */
    height: 40px; /* Feste Höhe */
    font-size: 22px; /* Größere Schrift */
    display: flex; /* Zentriert den Inhalt */
    align-items: center;
    justify-content: center;
    border: none; /* Entfernt den Standard-Rand */
    border-radius: 8px; /* Runde Ecken */
    cursor: pointer;
    gap: 25px;
    margin-bottom: 10px; /* Vertikaler Abstand zwischen den Buttons */
    margin-left: 42.5%;
  }

  .logOut-button {
    background: #dc3545;
    }
  
  body {
    background-color: #f3f4f6;
    font-family: Arial, sans-serif;
  }

</style>
