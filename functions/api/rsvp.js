export async function onRequest(context) {
  const db = context.env.DB;
  const url = new URL(context.request.url);

  // Tratamento de CORS para evitar problemas locais ou em produção
  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  if (context.request.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  if (context.request.method === "POST") {
    try {
      const data = await context.request.json();
      
      const result = await db.prepare(
        "INSERT INTO rsvp (name, availability, guests, poll, timestamp) VALUES (?, ?, ?, ?, ?)"
      )
      .bind(
        data.name || "Anônimo", 
        data.availability || "Nenhum dia", 
        data.guests || 0, 
        data.poll || "", 
        Date.now()
      )
      .run();

      return new Response(JSON.stringify({ success: true, result }), { 
        status: 200, 
        headers: { "Content-Type": "application/json", ...corsHeaders } 
      });
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), { 
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders }
      });
    }
  } 
  
  if (context.request.method === "GET") {
    try {
      const { results } = await db.prepare("SELECT * FROM rsvp ORDER BY timestamp ASC").all();
      return new Response(JSON.stringify(results), { 
        status: 200,
        headers: { "Content-Type": "application/json", ...corsHeaders } 
      });
    } catch (e) {
       return new Response(JSON.stringify({ error: e.message }), { 
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders }
      });
    }
  }

  return new Response("Method not allowed", { status: 405, headers: corsHeaders });
}
