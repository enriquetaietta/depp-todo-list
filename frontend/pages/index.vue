<template>
  <div class="main-container">
    <div class="content-container">
      <div class="content-main">
        <!-- Titolo principale -->
        <h1 class="page-title">TODO List</h1>

        <!-- SEPARATORE -->
        <div class="separator"></div>

        <!-- FILTRI -->
        <ToDoFilters @update="applyFilters" />

        <!-- Task Counter -->
        <div class="task-counter mb-4 text-lg font-bold text-gray-400">
          {{ todos.length }} task{{ todos.length !== 1 ? 's' : '' }}
        </div>

      <!-- Add Todo Form -->
      <TodoForm v-if="showForm"
        @close="handleCloseForm"
        />

        <!-- LISTA -->
        <div v-if="loading" class="text-center py-8">Loading...</div>
        <div v-else-if="todos.length === 0" class="text-center py-8 text-[#8b949e]">
          No todos found
        </div>
        <template v-else>
          <TodoItem v-for="t in todos" :key="t.id" :todo="t" @reload="applyFilters" />
        </template>

        <!-- Bottone per aggiungere nuovo todo -->
        <div class="fixed bottom-8 right-8">
        <!-- Floating Add Button -->
        <button
          v-if="!showForm"
          @click="showForm = true"
          class="fixed bottom-8 right-8 w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import TodoItem from "~/components/TodoItem.vue";
import ToDoFilters from "~/components/ToDoFilters.vue";
import TodoForm from "~/components/TodoForm.vue";
import { useTodos } from "~/composables/useTodos";

const { todos, fetchTodos, loading } = useTodos();
const showForm = ref(false);

// Carica i todo all'avvio
onMounted(() => {
  fetchTodos();
});

// Gestisce l'aggiornamento dei filtri
function applyFilters(filters) {
  // Aggiungi un piccolo ritardo per evitare chiamate multiple rapide
  setTimeout(() => {
    fetchTodos(filters);
  }, 100);
}

function handleCloseForm() {
  showForm.value = false;
  applyFilters({}); 
  // TODO -> Valutare come gestire il filtraggio dei dati, reset filtri (emit 'reset')?
  // gestione defineExpose?
}
</script>