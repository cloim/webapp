import { Get, Post } from "$lib/network.js";

export async function GET({ cookies, request }) {
    const token = cookies.get("token");
    const url = new URL(request.url);
    const method = url.searchParams.get("m");
    const action = url.searchParams.get("a");
    const param = JSON.parse(url.searchParams.get("p")) || {};

    let res;
    if (method == "GET") {
        res = await Get(`${action}`, param, token);
    } else if (method == "POST") {
        res = await Post(`${action}`, param, token);
    }

    const res_data = await res.json();
    let msg = "";
    let data;

    if (res.status !== 200) {
        msg = res_data.detail;
    } else {
        data = res_data;
    }

    return new Response(JSON.stringify({ status: res.status, message: msg, data: data }));
}