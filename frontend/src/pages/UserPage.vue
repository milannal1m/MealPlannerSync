<script setup>

  import { useRoute } from 'vue-router';
  import { defineEmits } from 'vue';
  import { ref, onMounted } from 'vue';
  import BackButton from '@/components/BackButton.vue';
  import AddButton from '../components/AddButton.vue';

  const route = useRoute();
  const items = ref([]);

  const emit = defineEmits(['removeItem']);

  onMounted(() => {
    if (route.query.items) {
      items.value = JSON.parse(route.query.items);
    }
  });
  
</script>

<template>
  <div class = "user-header">
    <BackButton />
    <h1>Connections</h1>
    <AddButton />
  </div>

  <ul class = "user-list">
    <li v-for="(item, index) in items" :key="item.id">
        <div class = "user-item user-name">{{ item.username }} 
          <button class="delete-button"
          @click="emit('removeItem', index)"><i class="fa-solid fa-trash"></i></button> </div>
      </li>
  </ul>

</template>

<style>

  .user-header {
    display: flex;
    align-items: center;
    gap: 10px; /* Abstand zwischen den Elementen */
  }

  .user-list {
    list-style: none;
    padding: 0;
  }

  .user-item {
    background: #ffffff;
    padding: 12px;
    margin: 8px 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 60%; /* Oder eine andere feste Breite, z. B. 400px */

    display: flex;
    justify-content: space-between; /* Hält Username links & Buttons rechts */
    align-items: center; /* Sorgt für gleiche Höhe */
  }

  .user-name {
    font-size: 20px;
    font-weight: bold	;
  }

  .delete-button {
  background: #dc3545;
  }

  .delete-button:hover {
  background: #c82333;
  }

</style>