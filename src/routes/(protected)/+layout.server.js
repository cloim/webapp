import { PUBLIC_APP_URI } from '$env/static/public';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, fetch }) => {
    const token = cookies.get("token");
    if (!token) {
        throw redirect(303, "/signin");
    }

    const res = await fetch(`${PUBLIC_APP_URI}/me`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (res.status !== 200) {
        throw redirect(303, "/signin");
    }

    const data = await res.json();
    delete data.upw;

    return {
        user: data
    };
};