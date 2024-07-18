import { PUBLIC_APP_URI } from '$env/static/public';

export async function POST({ cookies, request }) {
    const req_data = await request.json();
    req_data.status = "D";
    
    const res = await fetch(`${PUBLIC_APP_URI}/signup`, {
        method: "POST",
        body: JSON.stringify(req_data)
    });
    const res_data = await res.json();

    if (res.status !== 200) {
        cookies.set("token", "", { path: "/" });
        return new Response(JSON.stringify({
            status: res.status,
            detail: res_data.detail
        }));
    } else {
        if (req_data.status == "N") {
            cookies.set("token", res_data.access_token, { path: "/" });
            return new Response(JSON.stringify({
                status: res.status,
                detail: ""
            }));
        } else {
            cookies.set("token", "", { path: "/" });
            return new Response(JSON.stringify({
                status: 403,
                detail: "관리자의 승인이 필요합니다"
            }));
        }
    }
}