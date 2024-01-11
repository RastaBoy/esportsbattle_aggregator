export default {
    actions: {
    //   async api_request({ getters, dispatch }, { endpoint, headers, body}) {
    async api_request({ getters }, { endpoint, headers, body}) {
        let options = {
          headers: headers || {}
        }
  
        if (body) {
          options.method = 'POST'
          options.headers['Content-type'] = 'application/json'
          options.body = JSON.stringify(body)
        }
        
        let response = await fetch(getters.url+'/api/v1'+endpoint, options)
        response = await response.json()
        console.log(response)
        if (response.status != 200) {
            console.log("Ошибка!!!")
        }
        else {
            console.log(response.json)
        }
        // if (!response.result) {
        //   console.error(`Request ${endpoint} failed: (${response.error_class}) ${response.error_text}`)  
        //   throw new Error(response.error_text)
        // } else {
        //   return response.data
        // }
      },
    },
    getters: {
      url(){
        return process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:11011' : ''
      }
    }
  }