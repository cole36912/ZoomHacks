const VERSION = "v0.0.1";
const DATA_PATH_META = "data/meta/payload_info_{data}.json";
const DATA_PATH_NAMES = "data/meta/camera_names_{data}.json";
const DATA_PATH_BINARY_ORIGINAL = "data/original/binary/camera_data_{data}.bin";
const DATA_PATH_BINARY_MODIFIED = "data/modified/{mod}/binary/camera_data_{data}.bin";
const DATA = ["dppt", "hgss"];
const MODIFICATIONS = [];

document.getElementById("version").innerHTML = VERSION;
const app = document.getElementById("app");

function get_text(url) {
    const request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send(null);
    return request.responseText;
}

function get(url) {
    const request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send(null);
    return request.response;
}

function load_data(meta, data) {
    app.innerHTML = "";
}

function load_default_data(data) {
    const meta = JSON.parse(get_text(DATA_PATH_META.replace("{data}", data)));
    const binary_data = JSON.parse(get(DATA_PATH_BINARY_ORIGINAL.replace("{data}", data)));
    load_data(meta, binary_data);
}

{
    const data_selector = document.createElement("select");
    for(let item of DATA) {
        const option = document.createElement("option");
        option.innerHTML = `${option.value = item} default`;
        data_selector.appendChild(option);
    }
    app.appendChild(data_selector);
    app.appendChild(document.createElement("br"));
    const use_data = document.createElement("button");
    use_data.innerHTML = "Use data";
    use_data.onclick = () => load_default_data(data_selector.value);
    app.appendChild(use_data);
    const upload_data = document.createElement("button");
    upload_data.innerHTML = "Use data from disk...";
    app.appendChild(upload_data);
}