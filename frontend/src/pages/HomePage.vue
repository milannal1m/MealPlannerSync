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

</script>

<template>
  <h1>Meal Planner</h1>
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
  
  body {
    background-color: #f3f4f6;
    font-family: Arial, sans-serif;
  }

</style>
