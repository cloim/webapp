import { PUBLIC_APP_URI } from '$env/static/public';

export async function POST({ cookies, request }) {
    const token = cookies.get("token");
    const req_data = await request.json();
    
    const options = {
        method: req_data.m,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    }

    if (req_data.m == "POST" && req_data.p) {
        options.body = JSON.stringify(req_data.p);
    }
    
    let url;
    if (req_data.m == "GET" && req_data.p) {
        const query = Object.keys(req_data.p)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(req_data.p[key])}`)
            .join('&');
        url = `${PUBLIC_APP_URI}/${req_data.a}?${query}`;
    } else {
        url = `${PUBLIC_APP_URI}/${req_data.a}`;
    }
    
    return await fetch(url, options);
}