const api = async (
    url,
    options = {}
) => {
    const response = await fetch(
        url,
        {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {}),
            },
            credentials: "include",
            ...options,
        }
    );

    const data = await response
        .json()
        .catch(() => ({}));

    if (!response.ok) {
        throw new Error(
            data.detail ||
            data.message ||
            "Request failed."
        );
    }

    return data;
};


async function checkAuth() {
    try {
        return await api(
            "/api/auth/me"
        );
    } catch {
        return {
            authenticated: false,
        };
    }
}


async function registerUser(
    username,
    email,
    password,
    city
) {
    return api(
        "/api/auth/register",
        {
            method: "POST",
            body: JSON.stringify({
                username,
                email,
                password,
                city,
            }),
        }
    );
}


async function loginUser(
    username,
    password
) {
    return api(
        "/api/auth/login",
        {
            method: "POST",
            body: JSON.stringify({
                username,
                password,
            }),
        }
    );
}


async function logoutUser() {
    return api(
        "/api/auth/logout",
        {
            method: "POST",
        }
    );
}


async function loadStats() {
    return api(
        "/api/crime/stats"
    );
}


async function loadHotspots() {
    return api(
        "/api/crime/hotspots"
    );
}


async function loadForecast() {
    return api(
        "/api/crime/forecast"
    );
}


async function classifyFIR(
    text
) {
    return api(
        "/api/crime/fir",
        {
            method: "POST",
            body: JSON.stringify({
                text,
            }),
        }
    );
}


async function findSafeRoute(
    originLat,
    originLon,
    destinationLat,
    destinationLon
) {
    return api(
        "/api/route/safe",
        {
            method: "POST",
            body: JSON.stringify({
                origin_lat: originLat,
                origin_lon: originLon,
                destination_lat:
                    destinationLat,
                destination_lon:
                    destinationLon,
            }),
        }
    );
}


async function sendSOS(
    latitude,
    longitude,
    message
) {
    return api(
        "/api/sos/",
        {
            method: "POST",
            body: JSON.stringify({
                latitude,
                longitude,
                message,
            }),
        }
    );
}