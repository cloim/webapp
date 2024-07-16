import { PUBLIC_APP_URI } from '$env/static/public';

export async function POST({ cookies, request }) {
    const req_data = await request.json();
    const res = await fetch(`${PUBLIC_APP_URI}/signin`, {
        method: "POST",
        body: JSON.stringify(req_data),
    });
    const res_data = await res.json();

    if (res.status !== 200) {
        cookies.set("token", "", { path: "/" });
    } else {
        cookies.set("token", res_data.access_token, { path: "/" });
    }

    return new Response(JSON.stringify(res_data), {
        status: res.status,
        headers: {
            "Content-Type": "application/json"
        }
    });
}