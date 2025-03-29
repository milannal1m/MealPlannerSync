<script setup>

import { defineProps } from 'vue';
import { defineEmits } from 'vue';

defineProps({
  items: Array,
  searchQuery: String
});

const emit = defineEmits(['removeItem', 'editItem']);

</script>

<template>
  <ul class="meal-list">
    <li class = "meal-item"
      v-for="item in items.filter(i => 
        i.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
        i.meal.toLowerCase().includes(searchQuery.toLowerCase())
      )" 
      :key="item.date"
    >
      <div class="meal-info">
        <span class="meal-name">{{ item.meal }}  {{ item.date }}</span>
        <span class="meal-user">{{ item.username }}</span>
      </div>
      
      <div class="action-buttons">
        <button class="edit-button"
        @click = "emit('editItem', item)">Edit</button>
        <button class="delete-button"
        @click="emit('removeItem', index)">Delete</button> 
      </div>
    </li>
  </ul>
</template>

<style>

  .meal-list {
    list-style: none;
    padding: 0;
  }

  .meal-item {
    background: #ffffff;
    padding: 12px;
    margin: 10px 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .meal-info {
    display: flex;
    flex-direction: column;
  }

  .meal-name {
    font-size: 18px;
    font-weight: bold;
  }

  .meal-user {
    font-size: 14px;
    color: #666;
  }

    .edit-button,
  .delete-button {
    width: 100px;  /* Feste Breite */
    height: 50px; /* Feste Höhe */
    font-size: 24px; /* Größere Schrift */
    display: flex; /* Zentriert den Inhalt */
    align-items: center;
    justify-content: center;
    border: none; /* Entfernt den Standard-Rand */
    border-radius: 8px; /* Runde Ecken */
    cursor: pointer;
  }

  .edit-button {
  background: #ffc107;
  }

  .edit-button:hover {
  background: #e0a800;
  }

  .delete-button {
  background: #dc3545;
  }

  .delete-button:hover {
  background: #c82333;
  }

</style>