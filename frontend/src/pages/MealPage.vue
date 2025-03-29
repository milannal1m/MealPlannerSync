<script setup>

    import { ref, onMounted } from 'vue';
    import { useRoute } from 'vue-router'
    import BackButton from '@/components/BackButton.vue';

    const meal = useRoute().query;

    const name = ref('');
    const date = ref('');
    const ingredient = ref('');
    const ingredients = ref([]);
    const isEdit = ref(false);

    onMounted(() => {
        if(meal.username) {
            isEdit.value = true;
            name.value = meal.meal || '';
            date.value = meal.date || '';
            ingredients.value = meal.ingredients || [];
        }
    });

    const addIngredient = () => {
        if (ingredient.value.trim()) {
            ingredients.value.push(ingredient.value.trim());
            ingredient.value = '';
        }
    };

    const removeIngredient = (index) => {
        ingredients.value.splice(index, 1);
    };

    const saveMeal = () => {
        if (isEdit.value) {
            console.log('Meal updated:', {name: name.value, date: date.value, ingredients: ingredients.value })
        }
        else {
            console.log('Meal saved:', {name: name.value, date: date.value, ingredients: ingredients.value })
        }
    }

</script>

<template>

  <BackButton />
    
  <div class="p-4 max-w-md mx-auto bg-white rounded shadow">
    <h1 class="text-xl font-bold mb-4">{{ isEdit ? 'Edit Meal' : 'Create a Meal' }}</h1>
    
    <div>
        <label class="block mb-2">Name:</label>
        <input v-model="name" class="w-full p-2 border rounded mb-4" placeholder="Meal name" />
    </div>

    <div>
        <label class="block mb-2">Date:</label>
        <input v-model="date" type="date" class="w-full p-2 border rounded mb-4" />
    </div>

    <div class="flex mb-4">
        <label class="block mb-2">Add Ingredient:</label>
        <input v-model="ingredient" class="flex-1 p-2 border rounded mr-2" placeholder="New Ingredient" />
        <button @click="addIngredient" class="bg-blue-500 text-white px-4 py-2 rounded">Hinzufügen</button>
    </div>
    
    <ul>
      <li v-for="(item, index) in ingredients" :key="index" class="flex justify-between items-center p-2 border-b">
        {{ item }}
        <button @click="removeIngredient(index)" class="text-red-500">Löschen</button>
      </li>
    </ul>

    <button @click="saveMeal" class="mt-4 bg-green-500 text-white px-4 py-2 rounded">
      {{ isEdit? 'Save' : 'Create' }}
    </button>

  </div>
</template>

<style>
body {
  background-color: #f3f4f6;
  font-family: Arial, sans-serif;
}
</style>
