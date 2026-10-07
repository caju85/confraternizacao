import { onRequest as __api_rsvp_js_onRequest } from "/home/caio/confraternizacao/functions/api/rsvp.js"

export const routes = [
    {
      routePath: "/api/rsvp",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_rsvp_js_onRequest],
    },
  ]