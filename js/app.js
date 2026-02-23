// Frontend now talks to a backend API (Flask) which persists JSON on the server.
const API_BASE = "https://movie-collection-manager-42dbff9f12cd.herokuapp.com";
const PER_PAGE = 10;

let currentPage = 1;
let totalPages = 1;
let editingId = null;

const listEl = document.getElementById("movie-list");
const form = document.getElementById("movie-form");
const formTitle = document.getElementById("form-title");
const cancelEditBtn = document.getElementById("cancel-edit");
const totalCountEl = document.getElementById("total-count");
const avgRatingEl = document.getElementById("average-rating");
const currentPageEl = document.getElementById("current-page");
const totalPagesEl = document.getElementById("total-pages");
const prevBtn = document.getElementById("prev-page");
const nextBtn = document.getElementById("next-page");

async function fetchMovies(page = 1) {
  const res = await fetch(`${API_BASE}/movies?page=${page}`);
  if (!res.ok) throw new Error("Failed to load movies");
  return res.json();
}

async function fetchStats() {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error("Failed to load stats");
  return res.json();
}

function renderRows(movies) {
  listEl.innerHTML = "";
  movies.forEach(movie => {
    const row = document.createElement("tr");
    const imgSrc = movie.image_url || "https://via.placeholder.com/50x75?text=No+Image";
    row.innerHTML = `
      <td><img src="${imgSrc}" alt="${movie.title}" style="width:50px;height:75px;object-fit:cover;" onerror="this.src='https://via.placeholder.com/50x75?text=Broken'"></td>
      <td>${movie.title}</td>
      <td>${movie.genre}</td>
      <td>${movie.year}</td>
      <td>${movie.rating}</td>
      <td>
        <button class="btn" data-edit="${movie.id}">Edit</button>
        <button class="btn" data-delete="${movie.id}">Delete</button>
      </td>
    `;
    listEl.appendChild(row);
  });
}

async function loadPage(page) {
  try {
    const payload = await fetchMovies(page);
    currentPage = payload.page;
    totalPages = payload.total_pages || 1;
    currentPageEl.textContent = currentPage;
    totalPagesEl.textContent = totalPages;
    renderRows(payload.data);
    const s = await fetchStats();
    totalCountEl.textContent = s.total;
    avgRatingEl.textContent = (s.average_rating || 0).toFixed(1);
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage >= totalPages;
  } catch (err) {
    console.error(err);
    alert('Error loading data from server');
  }
}

form.addEventListener("submit", async e => {
  e.preventDefault();
  const title = document.getElementById("title").value.trim();
  const genre = document.getElementById("genre").value.trim();
  const year = Number(document.getElementById("year").value);
  const rating = Number(document.getElementById("rating").value);
  const image_url = document.getElementById("image_url").value.trim();

  if (!title || !genre || year < 1900 || rating < 1 || rating > 10) {
    alert("Please enter valid data.");
    return;
  }

  const body = { title, genre, year, rating, image_url };
  try {
    if (editingId === null) {
      await fetch(`${API_BASE}/movies`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
    } else {
      await fetch(`${API_BASE}/movies/${editingId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      editingId = null;
      cancelEditBtn.hidden = true;
      formTitle.textContent = "Add Movie";
    }
    form.reset();
    await loadPage(currentPage);
  } catch (err) {
    console.error(err);
    alert('Server error saving movie');
  }
});

cancelEditBtn.addEventListener("click", () => {
  editingId = null;
  form.reset();
  formTitle.textContent = "Add Movie";
  cancelEditBtn.hidden = true;
});

listEl.addEventListener("click", async (e) => {
  const editId = e.target.getAttribute('data-edit');
  const delId = e.target.getAttribute('data-delete');
  if (editId) {
    try {
      const res = await fetch(`${API_BASE}/movies/${editId}`);
      if (!res.ok) throw new Error('Not found');
      const movie = await res.json();
      document.getElementById("title").value = movie.title;
      document.getElementById("genre").value = movie.genre;
      document.getElementById("year").value = movie.year;
      document.getElementById("rating").value = movie.rating;
      document.getElementById("image_url").value = movie.image_url || "";
      editingId = movie.id;
      formTitle.textContent = "Edit Movie";
      cancelEditBtn.hidden = false;
    } catch (err) {
      alert('Failed to load movie');
    }
  }
  if (delId) {
    if (!confirm('Are you sure you want to delete this movie?')) return;
    try {
      const res = await fetch(`${API_BASE}/movies/${delId}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      // If deleting the last item on the page, ensure page remains valid
      await loadPage(currentPage);
    } catch (err) {
      alert('Failed to delete movie');
    }
  }
});

prevBtn.addEventListener('click', () => {
  if (currentPage > 1) loadPage(currentPage - 1);
});
nextBtn.addEventListener('click', () => {
  if (currentPage < totalPages) loadPage(currentPage + 1);
});

// initial load
loadPage(1);