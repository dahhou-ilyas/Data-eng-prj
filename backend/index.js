const axios = require("axios");


async function sendToNifi(params) {
    const response=axios.post("http://localhost:8081/contentListener",pyload)
}