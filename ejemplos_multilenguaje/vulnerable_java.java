// Ejemplo de código Java VULNERABLE
// Contiene vulnerabilidades de seguridad

import java.io.*;

public class VulnerableJava {
    
    // VULNERABILIDAD 1: Deserialización insegura
    public Object deserializarObjeto(byte[] data) throws Exception {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ObjectInputStream(bis);
        return ois.readObject();  // Peligroso sin validación
    }
    
    // VULNERABILIDAD 2: Ejecución de comandos sin sanitización
    public void ejecutarComando(String comando) throws Exception {
        Runtime.getRuntime().exec(comando);
    }
    
    // VULNERABILIDAD 3: SQL Injection
    public void consultaBaseDatos(String usuario) throws Exception {
        String query = "SELECT * FROM usuarios WHERE nombre = '" + usuario + "'";
        // Concatenación directa permite SQL injection
    }
    
    public static void main(String[] args) throws Exception {
        VulnerableJava app = new VulnerableJava();
        
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String entrada = reader.readLine();
        
        app.ejecutarComando(entrada);
    }
}
