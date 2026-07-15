<script setup lang="ts">
import BaseSection from '../base/BaseSection.vue'
</script>

<template>
  <BaseSection id="main">
    <h1 class="main-section__phrase">Un espacio para crear, sentir y crecer</h1>
  </BaseSection>
</template>

<style scoped>
.main-section__phrase {
  align-self: center;
  margin-block: auto;
  text-align: center;
  font-size: clamp(1.75rem, 5vw + 1rem, 3.5rem);
  font-weight: 600;
  line-height: 1.2;
}
</style>
