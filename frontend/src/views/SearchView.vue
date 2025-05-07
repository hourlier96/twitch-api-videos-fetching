<template>
    <v-autocomplete
        v-model="currentGameID"
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
                                <v-row>
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

        <template v-slot:no-data>
            <v-list-item>
                <v-list-item-title>No game found</v-list-item-title>
            </v-list-item>
        </template>
    </v-autocomplete>
    <div v-if="videoResult?.length">
        <v-list>
            <v-list-item
                v-for="video in videoResult"
                :key="video.id"
                :href="`https://www.twitch.tv/videos/${video.id}`"
                target="_blank"
            >
                <v-list-item-title>{{ video.title }}</v-list-item-title>
                <v-list-item-subtitle>{{
                    video.user_name
                }}</v-list-item-subtitle>
            </v-list-item>
        </v-list>
    </div>
    <div v-else-if="currentGameID">No video found for this game</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useDebounceFn } from "@vueuse/core";
import { getCategories } from "@/api/twitch.ts";

const currentGameID = ref("");
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
    currentGameID.value = game_id;
    loading.value = true;
    try {
        listenNewVideos(game_id);
    } catch (error) {
        console.error("Error fetching videos:", error);
        videoResult.value = { data: [] };
    } finally {
        loading.value = false;
    }
}

function listenNewVideos(game_id) {
    const eventSource = new EventSource(
        `http://127.0.0.1:8000/videos?game_id=${game_id}`
    );

    eventSource.onopen = () => {
        console.log("EventSource connected");
        //Everytime the connection gets extablished clearing the previous data from UI
    };

    //eventSource can have event listeners based on the type of event.
    //Bydefault for message type of event it have the onmessage method which can be used directly or this same can be achieved through explicit eventlisteners
    eventSource.addEventListener("newVideos", function (event) {
        const content = JSON.parse(event.data);
        console.log(content);
        videoResult.value = content;
    });

    //In case of any error, if eventSource is not closed explicitely then client will retry the connection a new call to backend will happen and the cycle will go on.
    eventSource.onerror = (error) => {
        console.error("EventSource failed", error);
        eventSource.close();
    };
}
</script>
