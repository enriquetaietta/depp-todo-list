<template>
  <div class="todo-card">
    <!-- Titolo + Priority -->
    <div class="flex justify-between items-center mb-2">
      <div class="todo-title">{{ todo.title }}</div>
      <div class="flex items-center">
        <button
          @click="deleteTodo"
          class="text-red-500 hover:text-red-700 focus:outline-none"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Descrizione -->
    <p v-if="todo.notes" class="todo-description">{{ todo.notes }}</p>

    <!-- Tags -->
    <div v-if="todo.tags && todo.tags.length > 0" class="mb-3">
      <TagItem v-for="tag in todo.tags" :key="tag" :text="tag" />
    </div>

    <!-- Stato + Toggle -->
    <div class="flex justify-between items-center pt-3 border-t border-[#30363d]">
      <button
        @click="toggle"
        class="toggle-button"
      >
      <span class="status-badge" :class="`status-${todo.state.toLowerCase()}`">
        {{ todo.state }}
      </span>
      </button>

      <span v-if="todo.priority" class="text-sm mr-2" :class="`priority-${todo.priority.toLowerCase()}`">
        Priority: {{ todo.priority }}
      </span>
    </div>
  </div>
</template>

<script setup>
import TagItem from "./TagItem.vue";
import { useTodos } from "~/composables/useTodos";

const emit = defineEmits(['reload']);

const props = defineProps({
  todo: {
    type: Object,
    required: true,
    validator: (value) => {
      // Validazione aggiuntiva per assicurarsi che l'oggetto todo abbia le proprietà necessarie
      return value &&
             typeof value.title === 'string' &&
             typeof value.state === 'string' &&
             (value.priority === undefined || typeof value.priority === 'string') &&
             (value.notes === undefined || typeof value.notes === 'string') &&
             (value.tags === undefined || Array.isArray(value.tags));
    }
  }
});

const { toggleState, fetchTodos } = useTodos();

async function toggle() {
  try {
    // Determina il nuovo stato
    let newState;
    if (props.todo.state === 'TODO') {
      newState = 'IN_PROGRESS';
    } else if (props.todo.state === 'IN_PROGRESS') {
      newState = 'DONE';
    } else {
      newState = 'TODO';
    }

    // Aggiorna lo stato
    await toggleState(props.todo.id, newState);
    console.log("toggleState -> start refresh?");
    // await fetchTodos(); // refresh lista
    emit("reload");
  } catch (error) {
    console.error('Error toggling todo state:', error);
  }
}

async function deleteTodo() {
  try {
    // Aggiorna lo stato a DELETED
    await toggleState(props.todo.id, 'DELETE');
    // await fetchTodos(); // refresh lista
    emit("reload");
  } catch (error) {
    console.error('Error deleting todo:', error);
  }
}
</script>