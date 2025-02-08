const connection = require('./src/config/db');

connection.query('SELECT 1 + 1 AS resultado', (err, results) => {
  if (err) {
    console.error('❌ Erro na query:', err);
    return;
  }
  console.log('🔥 Conectado ao MySQL!');
  console.log('🟢 Conexão bem-sucedida! Resultado:', results[0].resultado);
  connection.end(); // Fecha a conexão após o teste
});