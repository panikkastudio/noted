import axios from "axios";

function getURL(path) {
  return `http://localhost:8000${path}`;
}

export async function getAppConfig() {
  const d = await axios.get(getURL("/app/config"));
  return d.data;
}

export async function getCurrentTask() {
  const d = await axios.get(getURL("/task/current"));
  return d.data;
}

export async function advanceCurrentTask(data) {
  console.log(data);
  const d = await axios.post(getURL("/task/advance"), data);
  return d.data;
}
