<template>
    {{ apiResult }}
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getCategories } from "@/api/twitch.ts";

const apiResult = ref();

async function searchCategories(query: string) {
    apiResult.value = await getCategories({ game_label: query });
}

onMounted(() => {
    searchCategories("Test");
});
</script>

<style scoped>
#main-container {
    padding: var(--navigation-bar-height) 0px var(--navigation-bar-height) 0px;
}
</style>
