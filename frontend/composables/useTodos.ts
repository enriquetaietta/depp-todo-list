import axios from "axios";
import { useAppToast } from "~/composables/useToast";

// TODO -> Da gestire in un file .env
const API_URL = "http://localhost:8000/api/v1";

export function useTodos() {
  const todos = ref([]);
  const loading = ref(false);
  const { showError, showSuccess, showInfo, clearToast } = useAppToast();

  async function fetchTodos(params = {}) {
    loading.value = true;
    try {
      // Filtra i parametri per rimuovere valori vuoti
      const filteredParams = Object.fromEntries(
        Object.entries(params).filter(([_, v]) => v != null && v !== '')
      );

      console.log("Fetching todos with params:", filteredParams);

      const res = await axios.get(`${API_URL}/todo/`, {
        params: filteredParams
      });
      console.log(res);
      todos.value = res.data;
    } catch (error) {
      console.error('Error fetching todos:', error);
      todos.value = [];

      // Mostra un toast di errore
      showError('Failed to fetch todos. Please try again later.');
    } finally {
      loading.value = false;
    }
  }

  async function toggleState(id: string, newState: string) {
    console.log("Start toggleState -> " + id);
    try {
      const res = await axios.put(`${API_URL}/todo/${id}`, {
        state: newState
      });

      // Mostra un toast di successo
      showSuccess('Todo state updated successfully!');

      return res.data;
    } catch (error) {
      console.error('Error toggling todo state:', error);

      // Mostra un toast di errore
      showError('Failed to update todo state. Please try again.');

      throw error;
    }
  }

  async function createTodo(todoData: {
    title: string;
    notes?: string;
    priority?: string;
    tags?: string[];
  }) {
    try {
      // Show loading toast and store reference
      showInfo('Creating new todo...');

      // Crea l'oggetto da inviare all'API
      const payload = {
        title: todoData.title,
        notes: todoData.notes || null,
        priority: todoData.priority || 'LOW', // Default a LOW se non specificato
        tags: todoData.tags || []
      };

      // Chiama l'API per creare il nuovo todo
      const response = await axios.post(`${API_URL}/todo/`, payload);

      // Close the loading toast
      clearToast();

      // Show success toast
      showSuccess('Todo created successfully!');

      return response.data;
    } catch (error) {
      console.error('Error creating todo:', error);

      // Show error toast
      showError('Failed to create todo. Please try again.');
      throw error;
    }
  }

  return { todos, fetchTodos, toggleState, createTodo, loading };
}
