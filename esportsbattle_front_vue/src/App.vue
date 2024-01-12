<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <h1>ESportsBattle Site Aggregator</h1>
      </div>
      <v-spacer></v-spacer>
      <div>
        <h2>Текущее время в UTC: {{ utc_time }}</h2> 
      </div>
    </v-app-bar>

    <v-main>
      <AggregatorsInfo />
    </v-main>
  </v-app>
</template>

<script>
import AggregatorsInfo from './components/AggregatorsInfo';

export default {
  name: 'App',

  components: {
    AggregatorsInfo,
  },

  data: () => ({
    date: 0,
  }),
  mounted(){
    this.date = new Date()
  },
  created() {
    this.intervalId = setInterval(() => this.date = Date.now(), 1000); // Обновляем значения не чаще раза в секунду. А то и реже.
  },
  beforeDestroy() {
    if (this.intervalId) clearInterval(this.intervalId)
  },
  computed: {
    utc_time() {
      return (new Date(this.date)).toUTCString()
    }
  }
};
</script>
