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
    
  <div class="p-4 max-w-md mx-auto bg-white rounded shadow">
    <div class = "meal-header">
      <BackButton />
      <h1 class="text-xl font-bold mb-4">{{ isEdit ? 'Edit Meal' : 'Create a Meal' }}</h1>
    </div>
    
    <div class = "form-group">
        <label class="meal-name">Name:</label>
        <input v-model="name" placeholder="Meal name" />
    </div>

    <div class = "form-group">
        <label class="meal-name">Date:</label>
        <input v-model="date" type="date" />
    </div>

    <div class = "form-group">
        <label class="meal-name">Add Ingredient:</label>
        <input v-model="ingredient" class="input" placeholder="New Ingredient" />
        <button @click="addIngredient" class = "add-button-meal">+</button>
    </div>
    
    <ul class = "meal-list">
      <li v-for="(item, index) in ingredients" :key="index" class="meal-item">
        {{ item }}
        <button @click="removeIngredient(index)" class="delete-button"><i class="fa-solid fa-trash"></i></button>
      </li>
    </ul>

    <button @click="saveMeal" class="save-button">
      {{ isEdit? 'Save' : 'Create' }}
    </button>

  </div>
</template>

<style>
.meal-header {
  display: flex;
  align-items: center;
  gap: 10px; /* Abstand zwischen den Elementen */
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 100px; /* Einheitliche Breite für die Labels */
}

.form-group input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 250px; /* Breitere Eingabefelder */
}

.add-ingredient-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.add-ingredient-container input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.add-ingredient-container button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  width: 40%;
}

.add-ingredient-container button:hover {
  background-color: #218838;
}
  
.meal-list {
    list-style: none;
    padding: 0;
  }

  .meal-item {
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

  .add-button-meal {
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
        margin-left: 10px;
  }

  .delete-button {
  background: #dc3545;
  }

  .delete-button:hover {
  background: #c82333;
  }

  .save-button {
    background: #ffc107;
    font-size: 14px; /* Größere Schrift */
    font-weight: bold;
    display: flex; /* Zentriert den Inhalt */
    align-items: center; /* Zentriert vertikal */
    justify-content: center; /* Zentriert horizontal */
    border: none; /* Entfernt den Standard-Rand */
    border-radius: 8px; /* Runde Ecken */
    cursor: pointer;
    padding: 12px 18px; /* Abstand */
  }

  .save-button:hover {
  background: #e0a800;
  }

</style>
