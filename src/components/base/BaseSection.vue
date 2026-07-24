<script setup lang="ts">
defineProps<{ id?: string; fullHeight?: boolean }>()
defineSlots<{ default(): unknown }>()
</script>

<template>
  <section
    :id="id"
    class="base-section"
    :class="{ 'base-section--full': fullHeight }"
  >
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
}

.base-section--full {
  min-height: 100dvh;
}

.base-section__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: 1.25rem;
  padding-block: var(--section-padding);
}

@media (min-width: 640px) {
  .base-section__content {
    padding-inline: 2rem;
  }
}

@media (min-width: 1024px) {
  .base-section__content {
    padding-inline: 3rem;
  }
}
</style>
