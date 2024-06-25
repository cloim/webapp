import { Post } from "$lib/network.js";

export async function POST({ cookies, request }) {
    const req_data = await request.json();
    const res = await Post("signup", req_data);
    const res_data = await res.json();

    let msg = "";
    if (res.status !== 200) {
        cookies.set("token", "", { path: "/" });
        msg = res_data.detail;
    } else {
        cookies.set("token", res_data.access_token, { path: "/" });
    }

    return new Response(JSON.stringify({ status: res.status, message: msg }));
}