const TOPICS = [
  { id: "python", label: "Python", tag: "GIL · async · memory" },
  { id: "golang", label: "Go", tag: "goroutines · GC · channels" },
  { id: "mysql", label: "MySQL", tag: "indexes · ACID · InnoDB" },
  { id: "linux", label: "Linux", tag: "epoll · shell · signals" },
  { id: "networking", label: "Networking", tag: "TCP · HTTP · DNS" },
  { id: "operating-systems", label: "Operating Systems", tag: "processes · IPC" },
  { id: "redis", label: "Redis", tag: "cache · LRU · single-thread" },
  { id: "algorithms", label: "Algorithms", tag: "sort · heap · top-K" },
  { id: "system-design", label: "System Design", tag: "CAP · scaling · CDN" },
];

const listEl = document.getElementById("topic-list");
const renderedEl = document.getElementById("rendered");
const metaEl = document.getElementById("topic-meta");
const searchEl = document.getElementById("search");
const statsEl = document.getElementById("stats");

let activeId = null;

function renderNav(filter = "") {
  listEl.innerHTML = "";
  const q = filter.toLowerCase();
  TOPICS.filter(
    (t) => !q || t.label.toLowerCase().includes(q) || t.tag.toLowerCase().includes(q)
  ).forEach((topic) => {
    const btn = document.createElement("button");
    btn.className = topic.id === activeId ? "active" : "";
    btn.innerHTML = `${topic.label}<span class="tag">${topic.tag}</span>`;
    btn.onclick = () => loadTopic(topic.id);
    listEl.appendChild(btn);
  });
}

async function loadTopic(id) {
  activeId = id;
  renderNav(searchEl.value);
  const topic = TOPICS.find((t) => t.id === id);
  metaEl.innerHTML = `
    <span class="chip live">● live</span>
    <span class="chip">${topic.label}</span>
    <span class="chip">${id}.md</span>`;
  renderedEl.innerHTML = `<p style="color:var(--muted)">Loading…</p>`;
  try {
    const res = await fetch(`/api/topics/${id}`);
    const data = await res.json();
    renderedEl.innerHTML = marked.parse(data.content);
    const sections = (data.content.match(/^#{1,3} /gm) || []).length;
    statsEl.textContent = `${TOPICS.length} topics · ${sections} sections`;
  } catch (e) {
    renderedEl.innerHTML = `<p>Error loading topic: ${e.message}</p>`;
  }
}

searchEl.addEventListener("input", (e) => renderNav(e.target.value));

renderNav();
loadTopic("python");
