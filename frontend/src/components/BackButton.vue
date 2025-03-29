<script setup>

import { useRouter } from 'vue-router';

const router = useRouter();

const navigateBack = () => {
  router.push('/home'); 
};

</script>

<template>

  <button @click="navigateBack" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
    Back
  </button>
  
</template>