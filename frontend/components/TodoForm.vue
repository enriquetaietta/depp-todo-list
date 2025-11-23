<template>
  <div class="todo-card p-4">
    <form @submit.prevent="handleSaveTodo" class="space-y-6">

      <!-- TITLE -->
      <div class="flex items-center justify-between">
        <label for="title" class="text-sm font-medium text-gray-300 w-1/3">Title</label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          class="w-2/3 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- NOTES -->
      <div class="flex items-start justify-between">
        <label for="notes" class="text-sm font-medium text-gray-300 w-1/3 pt-1">Notes</label>
        <textarea
          id="notes"
          v-model="formData.notes"
          rows="3"
          class="w-2/3 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <!-- PRIORITY -->
      <div class="flex items-center justify-between">
        <label class="text-sm font-medium text-gray-300 w-1/3">Priority</label>

        <div class="flex space-x-2 w-2/3 justify-end">
          <button
            type="button"
            @click="formData.priority = 'LOW'"
            :class="priorityClasses('LOW')"
          >
            Low
          </button>

          <button
            type="button"
            @click="formData.priority = 'MEDIUM'"
            :class="priorityClasses('MEDIUM')"
          >
            Medium
          </button>

          <button
            type="button"
            @click="formData.priority = 'HIGH'"
            :class="priorityClasses('HIGH')"
          >
            High
          </button>
        </div>
      </div>

      <!-- TAGS -->
      <div class="flex items-center justify-between">
        <label for="tags" class="text-sm font-medium text-gray-300 w-1/3">Tags</label>
        <input
          id="tags"
          v-model="formData.tags"
          type="text"
          placeholder="Comma separated tags"
          class="w-2/3 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- BUTTONS -->
      <div class="flex justify-center space-x-4 pt-6 border-t border-[#30363d]">
        <button
          type="button"
          @click="handleCancel"
          class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 
                 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          Cancel
        </button>

        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Save
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useTodos } from '~/composables/useTodos';

const { createTodo, fetchTodos } = useTodos();

const formData = ref({
  title: '',
  notes: '',
  priority: 'LOW',
  tags: ''
});

const emit = defineEmits(['close']);

/* Tailwind classes reattive per i bottoni di priority */
const priorityClasses = (value) => {
  return [
    "px-3 py-1 rounded-xl text-white transition-colors",
    "focus:outline-none focus:ring-2 focus:ring-blue-500",
    formData.value.priority === value
      ? "bg-blue-600"
      : "bg-gray-700 hover:bg-gray-600"
  ];
};

function handleSaveTodo() {
  console.log("QUESTO HANDLESAVETODO VIENE CHIAMATONEL TODOFORM");
  createTodo(formData.value)
    .then(async () => {
      resetForm();
      emit("close");
      await fetchTodos();
    })
    .catch(error => {
      console.error('Error creating todo:', error);
    });
}

function handleCancel() {
  resetForm();
  emit('close');
}

function resetForm() {
  formData.value = {
    title: '',
    notes: '',
    priority: 'LOW',
    tags: ''
  };
}
</script>
