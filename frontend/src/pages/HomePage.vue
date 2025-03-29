<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import SearchBar from '../components/SearchBar.vue';
import MealList from '../components/MealList.vue';
import AddButton from '../components/AddButton.vue';
import UserButton from '../components/UserButton.vue';

const searchQuery = ref('');
const items = ref([
  { username: 'Alice', date: '2024-03-19', meal: 'Pancakes', ingredients: ["Flour", "Egg"]},
  { username: 'Bob', date: '2024-03-18', meal: 'Tacos' },
  { username: 'Charlie', date: '2024-03-17', meal: 'Steak' },
]);

const router = useRouter();

const removeItem = (index) => {
  items.value.splice(index, 1);
};

const editItem = (meal) => {
  router.push({
    path: '/meal',
    query: meal
  })
};

</script>

<template>
  <h1>Meal Planner</h1>
  <div class="p-4 max-w-md mx-auto">
    <UserButton :items="items" @removeItem="removeItem" />
    <SearchBar v-model="searchQuery" />
    <AddButton />
    <MealList :items="items" :searchQuery="searchQuery" @removeItem="removeItem" @editItem="editItem"/>
  </div>
</template>

<style>
  .add-button {
    display: inline-block;
    margin-bottom: 15px;
    background: #28a745;
    font-size: 20px;
    padding: 8px 12px;
  }

  .add-button:hover {
    background: #218838;
  }
</style>
