import { PUBLIC_APP_URI } from '$env/static/public';

export const Get = async (endpoint, data, auth_token) => {
    const options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    }
    if (auth_token) options.headers["Authorization"] = `Bearer ${auth_token}`;

    let url;
    if (data) {
        const query = Object.keys(data)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(data[key])}`)
            .join('&');
        url = `${PUBLIC_APP_URI}/${endpoint}?${query}`;
    } else {
        url = `${PUBLIC_APP_URI}/${endpoint}`;
    }

    return await fetch(url, options);
}

export const Post = async (endpoint, data, auth_token) => {
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    }
    if (auth_token) options.headers["Authorization"] = `Bearer ${auth_token}`;
    if (data) options.body = JSON.stringify(data);

    const url = `${PUBLIC_APP_URI}/${endpoint}`;

    return await fetch(url, options);
}
