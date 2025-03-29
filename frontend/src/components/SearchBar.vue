<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
</script>

<template>
  <input
    type="text"
    class="search-bar"
    placeholder="Suche nach Benutzer oder Text..."
    :value="modelValue"
    @input="emit('update:modelValue', $event.target.value)"
  />
</template>

<style>
  .search-bar {
    width: 50%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
</style>