<script setup lang="ts">
defineProps<{ id?: string }>()
defineSlots<{ default(): unknown }>()
</script>

<template>
  <section :id="id" class="base-section">
    <div class="base-section__content">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.base-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  min-height: 100dvh;
}

.base-section__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: 1rem;
}

@media (min-width: 640px) {
  .base-section__content {
    padding-inline: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .base-section__content {
    padding-inline: 2.5rem;
  }
}
</style>
