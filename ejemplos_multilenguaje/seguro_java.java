// Ejemplo de código Java SEGURO
// Implementa prácticas seguras de programación

import java.io.*;
import java.sql.*;
import java.util.regex.*;

public class SeguroJava {
    
    // Deserialización segura con validación
    public Object deserializarObjetoSeguro(byte[] data, Class<?> expectedClass) throws Exception {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ValidatingObjectInputStream(bis, expectedClass);
        return ois.readObject();
    }
    
    // Ejecución de comandos con ProcessBuilder (más seguro)
    public String ejecutarComandoSeguro(String comando) throws Exception {
        // Lista blanca de comandos permitidos
        String[] comandosPermitidos = {"ls", "pwd", "date"};
        
        boolean permitido = false;
        for (String cmd : comandosPermitidos) {
            if (comando.equals(cmd)) {
                permitido = true;
                break;
            }
        }
        
        if (!permitido) {
            throw new SecurityException("Comando no permitido");
        }
        
        ProcessBuilder pb = new ProcessBuilder(comando);
        Process process = pb.start();
        
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(process.getInputStream())
        );
        return reader.readLine();
    }
    
    // Consulta SQL segura con PreparedStatement
    public void consultaBaseDatosSegura(String usuario, Connection conn) throws SQLException {
        String query = "SELECT * FROM usuarios WHERE nombre = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, usuario);  // Previene SQL injection
        ResultSet rs = pstmt.executeQuery();
    }
    
    // Validación de entrada
    public boolean validarEntrada(String entrada) {
        Pattern patron = Pattern.compile("^[a-zA-Z0-9\\s]+$");
        Matcher matcher = patron.matcher(entrada);
        return matcher.matches();
    }
    
    public static void main(String[] args) throws Exception {
        SeguroJava app = new SeguroJava();
        
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String entrada = reader.readLine();
        
        if (app.validarEntrada(entrada)) {
            System.out.println("Entrada válida: " + entrada);
        } else {
            System.out.println("Entrada rechazada por validación");
        }
    }
}
