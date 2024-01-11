<template>
  <v-card
    elevation="2"
    shaped
  >
    <v-card-title>
      <h3>Список новых матчей</h3>
    </v-card-title>
    <v-card-subtitle>
      <h4>Данное приложение собирает все новые матчи по дисциплинам CS2 и Футболу с сайта ESportsBattle.</h4>
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-alert
      type="error"
      v-if="error.state"
    >
      {{ error.message }}
    </v-alert>
    <v-card-text>
      <div style="text-align: center;" v-if="loading">
        <Loader />
      </div>
      <div v-else>
        <v-data-table
          dense
          :headers="headers"
          :items="matches"
          class="elevation-1"
        >
        </v-data-table>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
  import {mapGetters} from 'vuex'
  import Loader from './ui/Loader.vue'

  export default {
    name: 'AggregatorsInfo',
    components: {
      Loader
    },
    data: () => ({
      loading: true,
      error: {
        state: false,
        message: ""
      }
    }),
    async mounted() {
      while(this.loading) {
        try 
        {
          await this.$store.dispatch('load_matches')
          this.loading = false
          this.error.state = false
          break
        } 
        catch(error) 
        {
          console.log(error)
          this.error.state = true
          this.error.message = error.message
          this.sleep(5000)
        }
      }
    },
    methods: {
      sleep(milliseconds) {
        const date = Date.now();
        let currentDate = null;
        do {
          currentDate = Date.now();
        } while (currentDate - date < milliseconds);
      }
    },
    computed: {
      ...mapGetters(['matches', ]),
      headers() {
        return [
          {
            text: "id",
            align: "start",
            value: "id"
          },
          {
            text: "Дата",
            value: "date"
          },
          {
            text: "Время",
            value : "time"
          },
          {
            text: "Название дисциплины",
            value: "discipline_name"
          },
          {
            text: "Название чемпионата",
            value: "tournament_name"
          },
          {
            text: "Участник №1",
            value: "participant1_name"
          },
          {
            text: "Участник №2",
            value: "participant2_name"
          }
        ]
      }

    },
  }
</script>
