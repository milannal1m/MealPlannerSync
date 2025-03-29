<script setup>

    import { defineProps } from 'vue';
    import { defineEmits } from 'vue';

    defineProps({
    items: Array,
    searchQuery: String
    });

    const emit = defineEmits(['removeItem']);

</script>

<template>

  <ul class="space-y-4">
    <li 
      v-for="item in items.filter(i => 
        i.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
        i.meal.toLowerCase().includes(searchQuery.toLowerCase())
      )" 
      :key="item.date"
      class="border p-4 rounded shadow flex justify-between items-center"
    >

      <div class="font-bold">{{ item.username }} <button class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
        @click="emit('removeItem', index)">🗑️</button> </div>
        
    </li>
  </ul>

</template>