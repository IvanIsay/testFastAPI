import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";

const API = "http://localhost:5000/v1/usuarios/";

export default function App() {

  const [usuarios, setUsuarios] = useState([]);
  const [nombre, setNombre] = useState("");
  const [edad, setEdad] = useState("");
  const [id, setId] = useState("");


   {/* Funcion Para consutar Usuarios*/}
  const obtenerUsuarios = async () => {
    try {
      const response = await fetch(API);
      const datos = await response.json();
      setUsuarios(datos.usuarios);
    } catch (error) {
      console.error(error);
    }
  };

  {/* Funcion p ara guardar Usuarios*/}
  const crearUsuario = async () => {
    if (!id || !nombre || !edad) return;

    await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: parseInt(id),
        nombre,
        edad: parseInt(edad),
      }),
    });

    obtenerUsuarios();
    setNombre("");
    setEdad("");
    setId("");
  };

  {/* Funcion para elimnar Usarios*/}
  const eliminarUsuario = async (id) => {
    await fetch(API + id, {
      method: "DELETE",
    });

    obtenerUsuarios();
  };

  useEffect(() => {
    obtenerUsuarios();
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.page}>
      <View style={styles.container}>
        <Text style={styles.title}>Gestión de Usuarios FastAPI</Text>

        {/* FORMULARIO */}
        <View style={styles.form}>
          <TextInput
            placeholder="ID"
            value={id}
            onChangeText={setId}
            style={styles.input}
          />
          <TextInput
            placeholder="Nombre"
            value={nombre}
            onChangeText={setNombre}
            style={styles.input}
          />
          <TextInput
            placeholder="Edad"
            value={edad}
            onChangeText={setEdad}
            style={styles.input}
          />

          <TouchableOpacity style={styles.button} onPress={crearUsuario}>
            <Text style={styles.buttonText}>Agregar Usuario</Text>
          </TouchableOpacity>
        </View>

        {/* LISTA */}
        <FlatList
          data={usuarios}
          keyExtractor={(item) => item.id.toString()}
          scrollEnabled={false}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View>
                <Text style={styles.cardTitle}>{item.nombre}</Text>
                <Text style={styles.cardSubtitle}>
                  ID: {item.id} | Edad: {item.edad}
                </Text>
              </View>

              <TouchableOpacity
                style={styles.deleteButton}
                onPress={() => eliminarUsuario(item.id)}
              >
                <Text style={styles.deleteText}>Eliminar</Text>
              </TouchableOpacity>
            </View>
          )}
        />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: {
    flexGrow: 1,
    backgroundColor: "#f4f6f8",
    alignItems: "center",
    paddingVertical: 40,
  },
  container: {
    width: "90%",
    maxWidth: 700,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 30,
    textAlign: "center",
  },
  form: {
    backgroundColor: "#ffffff",
    padding: 20,
    borderRadius: 12,
    marginBottom: 30,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
    backgroundColor: "#fafafa",
  },
  button: {
    backgroundColor: "#2563eb",
    padding: 15,
    borderRadius: 8,
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
  card: {
    backgroundColor: "#ffffff",
    padding: 20,
    borderRadius: 12,
    marginBottom: 15,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 6,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
  },
  cardSubtitle: {
    color: "#666",
    marginTop: 4,
  },
  deleteButton: {
    backgroundColor: "#ef4444",
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 6,
  },
  deleteText: {
    color: "#fff",
    fontWeight: "bold",
  },
});
