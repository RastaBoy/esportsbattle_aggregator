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
    //
  }),
};
</script>
