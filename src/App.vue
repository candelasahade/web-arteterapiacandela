<script setup lang="ts">
import NavBar from '@/components/base/NavBar.vue'
import SiteFooter from '@/components/base/SiteFooter.vue'
import MainSection from '@/components/sections/MainSection.vue'
import ArtTherapySection from '@/components/sections/ArtTherapySection.vue'
import AboutSection from '@/components/sections/AboutSection.vue'
import FaqSection from '@/components/sections/FaqSection.vue'
import ContactSection from '@/components/sections/ContactSection.vue'
</script>

<template>
  <a class="skip-link" href="#main">Saltar al contenido principal</a>
  <NavBar />
  <main>
    <MainSection />
    <ArtTherapySection />
    <AboutSection />
    <FaqSection />
    <ContactSection />
  </main>
  <SiteFooter />
</template>

<style scoped></style>
