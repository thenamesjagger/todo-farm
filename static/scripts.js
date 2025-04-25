function toggleCompleted() {
    const container = document.getElementById("completed-container");
    const button = document.querySelector(".toggle-completed");
  
    if (container.classList.contains("hidden")) {
      container.classList.remove("hidden");
      button.textContent = "Hide Completed Tasks";
    } else {
      container.classList.add("hidden");
      const count = button.dataset.completedCount || "0";
      button.textContent = `Show Completed Tasks (${count})`;
    }
  }
  