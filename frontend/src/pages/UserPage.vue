<script setup>

  import { useRoute } from 'vue-router';
  import { defineEmits } from 'vue';
  import { ref, onMounted } from 'vue';
  import BackButton from '@/components/BackButton.vue';

  const route = useRoute();
  const items = ref([]);

  const emit = defineEmits(['removeItem']);

  onMounted(() => {
    if (route.query.items) {
      items.value = JSON.parse(route.query.items);
      console.log('Items:', items.value);  // Hier überprüfen, ob die Items korrekt empfangen werden
    }
  });
  
</script>

<template>
  
  <BackButton />
  <h1>Connections</h1>
  
  <ul>
    <li v-for="item in items" :key="item.id">
        <div class="font-bold">{{ item.username }} <button class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
          @click="emit('removeItem', index)">🗑️</button> </div>
      </li>
  </ul>

</template>