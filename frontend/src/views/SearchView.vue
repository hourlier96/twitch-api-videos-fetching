<template>
    <v-autocomplete
        :items="categoryResult?.data"
        label="Search for a game"
        :loading="loading"
        :no-results="!categoryResult?.length"
        :no-results-text="'No results found'"
        item-title="name"
        item-value="id"
        @input="debouncedSearchCategories($event.target.value)"
    >
        <template #prepend>
            <v-icon>mdi-magnify</v-icon>
        </template>

        <template v-slot:item="{ props, item }">
            <v-list-item
                v-bind="props"
                :key="item.raw.id"
                @click="() => searchVideos(item.raw.id)"
            >
                <template v-slot:prepend>
                    <v-avatar size="40" rounded="sm" class="mr-3">
                        <v-img :src="item.raw.box_art_url" cover>
                            <template v-slot:placeholder>
                                <v-row
                                    class="fill-height ma-0"
                                    align="center"
                                    justify="center"
                                >
                                    <v-progress-circular
                                        indeterminate
                                        color="grey-lighten-5"
                                    ></v-progress-circular>
                                </v-row>
                            </template>
                        </v-img>
                    </v-avatar>
                </template>
            </v-list-item>
        </template>
    </v-autocomplete>
    <div v-if="videoResult?.data?.length">
        <v-list>
            <v-list-item-group>
                <v-list-item
                    v-for="video in videoResult.data"
                    :key="video.id"
                    :href="`https://www.twitch.tv/videos/${video.id}`"
                    target="_blank"
                >
                    <v-list-item-content>
                        <v-list-item-title>{{ video.title }}</v-list-item-title>
                        <v-list-item-subtitle>{{
                            video.user_name
                        }}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
        </v-list>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useDebounceFn } from "@vueuse/core";

import { getCategories, getVideos } from "@/api/twitch.ts";

const categoryResult = ref();
const videoResult = ref();
const loading = ref(false);

async function searchCategories(query: string) {
    loading.value = true;
    try {
        const response = await getCategories({ game_label: query });
        if (response.status === 200) {
            categoryResult.value = response.data;
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
        categoryResult.value = { data: [] };
    } finally {
        loading.value = false;
    }
}

const debouncedSearchCategories = useDebounceFn((label) => {
    searchCategories(label);
}, 300);

async function searchVideos(game_id) {
    loading.value = true;
    try {
        const response = await getVideos({ game_id });
        if (response.status === 200) {
            videoResult.value = response.data;
        }
    } catch (error) {
        console.error("Error fetching videos:", error);
        videoResult.value = { data: [] };
    } finally {
        loading.value = false;
    }
}
</script>

<style scoped>
#main-container {
    padding: var(--navigation-bar-height) 0px var(--navigation-bar-height) 0px;
}
</style>
