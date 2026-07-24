<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import NavBar from '@/components/base/NavBar.vue'
import SiteFooter from '@/components/base/SiteFooter.vue'
import MainSection from '@/components/sections/MainSection.vue'
import ArtTherapySection from '@/components/sections/ArtTherapySection.vue'
import AboutSection from '@/components/sections/AboutSection.vue'
import FaqSection from '@/components/sections/FaqSection.vue'
import ContactSection from '@/components/sections/ContactSection.vue'

const { t } = useI18n()
</script>

<template>
  <a class="skip-link" href="#main">{{ t('skipLink') }}</a>
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
