async function searchCity() {
    const city = document.getElementById("city").value;
    const API_KEY = "292e20dbde40e84f68dfba95d09234a8";  // Replace

    document.getElementById("output").innerText = "Loading...";

    // Step 1: Get latitude + longitude
    const geoURL =
        `https://api.openweathermap.org/geo/1.0/direct?q=${city}&limit=1&appid=${API_KEY}`;

    const geoRes = await fetch(geoURL);
    const geoData = await geoRes.json();

    if (geoData.length === 0) {
        document.getElementById("output").innerText = "City not found!";
        return;
    }

    const lat = geoData[0].lat;
    const lon = geoData[0].lon;

    // Step 2: Get weather using coordinates
    const weatherURL =
        `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${API_KEY}`;

    const weatherRes = await fetch(weatherURL);
    const weatherData = await weatherRes.json();

    // Display result
    document.getElementById("output").innerText =
        `City: ${weatherData.name}\n` +
        `Temperature: ${weatherData.main.temp} °C\n` +
        `Humidity: ${weatherData.main.humidity}%\n` +
        `Wind: ${weatherData.wind.speed} m/s\n` +
        `Weather: ${weatherData.weather[0].description}`;
}
