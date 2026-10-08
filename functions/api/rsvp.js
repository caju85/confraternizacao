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
      
      // Sanitização básica
      let name = (data.name || "").toString().trim().substring(0, 50);
      if (!name) name = "Anônimo";
      name = name.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      
      let availability = (data.availability || "Nenhum dia").toString().substring(0, 100).replace(/</g, "&lt;").replace(/>/g, "&gt;");
      let poll = (data.poll || "").toString().substring(0, 100).replace(/</g, "&lt;").replace(/>/g, "&gt;");
      
      let guests = parseInt(data.guests);
      if (isNaN(guests) || guests < 0) guests = 0;
      if (guests > 10) guests = 10; // Limite razoável para evitar estourar estatísticas
      
      // Check for duplicate name
      const existing = await db.prepare("SELECT id FROM rsvp WHERE LOWER(name) = LOWER(?)").bind(name).first();
      
      if (existing) {
        return new Response(JSON.stringify({ error: "Este nome já preencheu a pesquisa." }), { 
          status: 400, 
          headers: { "Content-Type": "application/json", ...corsHeaders } 
        });
      }
      
      const result = await db.prepare(
        "INSERT INTO rsvp (name, availability, guests, poll, timestamp) VALUES (?, ?, ?, ?, ?)"
      )
      .bind(
        name, 
        availability, 
        guests, 
        poll, 
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
