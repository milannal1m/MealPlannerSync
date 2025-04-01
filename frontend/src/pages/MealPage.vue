<script>

    import BackButton from '@/components/BackButton.vue';
                                                                                                                                                                                                                                                                                                                                                          
    export default {

      data() {
        return {
          id: 0,
          name: "",
          date: "",
          ingredient: "",
          amount: null,
          ingredients: [],
          isEdit: false,
          meal: null,
          owner: "",
          username: sessionStorage.getItem('user')
        };
      },

      mounted() {

        this.meal = this.$route.query;

        if (this.meal && Object.keys(this.meal).length > 0) {
          this.isEdit = true;
          this.id = this.meal.id;
          this.owner = this.meal.owner;
          this.name = this.meal.name;
          this.date = new Date(this.meal.planned_for);
          this.date.setDate(this.date.getDate() + 1);
          this.date = this.date.toISOString().split('T')[0];

          fetch("http://localhost/meal/" + this.owner + "/meals/"+ this.id + "/ingredients")
          .then(response => response.json())
          .then(data => {
            this.ingredients = data;
            console.log(this.ingredients)
          })
          .catch(error => {
            console.error("Error:", error);
            this.error = error;
          });

          this.ingredients = this.meal.ingredients ? JSON.parse(this.meal.ingredients) : [];
        }

      },

      components: {
        BackButton
      },

      methods: {
        createMeal(name, date) {
          if(this.username == this.owner) {
          const url = new URL("http://localhost/" + this.username + "/test/meals"); 
          url.searchParams.append("name", name);
          url.searchParams.append("date", date);

          fetch(url, {
            method: "Post"
          })
          .then(response => response.json())
          .then(data => console.log("Erfolgreich erstellt:", data))
          .catch(error => {
            console.error("Error:", error);
          });
        }
        else 
          alert("You are not the owner of this meal and cannot edit it.");
        },

        addIngredient(name, amount) {
          if(this.username == this.owner) {
          const url = new URL("http://localhost/meal/" + this.username + "/meals/" + this.id + "/ingredients"); 
          url.searchParams.append("name", name);
          url.searchParams.append("amount", amount);

          fetch(url, {
            method: "Post"
          })
          .then(response => response.json())
          .then(data => console.log("Erfolgreich erstellt:", data))
          .catch(error => {
            console.error("Error:", error);
          });
          } else 
            alert("You are not the owner of this meal and cannot add ingredients.");
          },

        removeIngredient(index) {
          if(this.username == this.owner) {
          fetch("http://localhost/meal/" + this.username + "/meals/" + this.id + "/ingredients/" + index, {
          method: "DELETE"
          })
          .then(response => {
            if (!response.ok) {
              throw new Error("Fehler beim Löschen");
            }
          console.log("Meal gelöscht");
          })
          .catch(error => console.error("Fehler:", error));
        }
        else 
          alert("You are not the owner of this meal and cannot remove ingredients.");
        }
      }
  };

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

    <div v-show="isEdit" class = "form-group">
        <label class="meal-name">Add Ingredient:</label>
        <input v-model="ingredient" class="input" placeholder="New Ingredient" />
        <input v-model="amount" class="input" placeholder="Amount" />
        <button @click="addIngredient(ingredient, amount)" class = "add-button-meal">+</button>
    </div>
    
    <ul class = "meal-list">
      <li v-for="ingredient in this.ingredients" :key="ingredient.id" class="meal-item">
        {{ ingredient.name }} ({{ ingredient.amount }})
        <button @click="removeIngredient(ingredient.id)" class="delete-button"><i class="fa-solid fa-trash"></i></button>
      </li>
    </ul>

    <button @click="createMeal(name, date)" class="save-button">
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
