<template>
  <div class="filters-container">
    <!-- Search Bar -->
    <input
      v-model="search"
      @input="emitUpdate"
      class="filter-input"
      placeholder="Search by title..."
    />

    <!-- Priority -->
    <select v-model="priority" @change="emitUpdate" class="filter-select">
      <option value="">All Priorities</option>
      <option value="LOW">Low</option>
      <option value="MEDIUM">Medium</option>
      <option value="HIGH">High</option>
    </select>

    <!-- Status -->
    <select v-model="state" @change="emitUpdate" class="filter-select">
      <option value="">All Statuses</option>
      <option value="ACTIVE">Active</option>
      <option value="TODO">Todo</option>
      <option value="IN_PROGRESS">In Progress</option>
      <option value="DONE">Done</option>
    </select>

    <!-- Sort -->
    <select v-model="sort" @change="emitUpdate" class="filter-select">
      <option value="">Default Sort</option>
      <option value="created_at">Creation Date</option>
      <option value="modified_at">Modified Date</option>
      <option value="priority">Priority</option>
      <option value="state">State</option>
    </select>
  </div>
</template>

<script setup>
const emit = defineEmits(["update"]);

const search = ref("");
const priority = ref("");
const state = ref("");
const sort = ref("");

function emitUpdate() {
  // Crea un oggetto con solo i filtri che hanno un valore
  const filters = {};

  if (search.value) filters.title = search.value;
  if (priority.value) filters.priority = priority.value;
  if (state.value) filters.state = state.value;
  if (sort.value) filters.sortby = sort.value;

  emit("update", filters);
}
</script>