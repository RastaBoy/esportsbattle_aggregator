export default {
    state: {
        matches: [],
    },
    getters : {
        matches(state) {
            return state.matches
        }
    },
    mutations : {
        set_matches(state, data) {
            state.matches = data
        }
    },
    actions : {
        async load_matches(ctx) {
            let response = await ctx.dispatch('api_request', {
                endpoint: '/matches/get_all'
            })
            ctx.commit('set_matches', response)
            return response
        }
    },
}