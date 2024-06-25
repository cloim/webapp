import { redirect } from '@sveltejs/kit';
import { Get } from "$lib/network.js";

export const load = async ({ cookies }) => {
    // const token = cookies.get("token");
    // if (!token) {
    //     throw redirect(303, "/signin");
    // }

    // const res = await Get("me", {}, token);
    // if (res.status !== 200) {
    //     throw redirect(303, "/signin");
    // }

    // const data = await res.json();
    // delete data.upw;

    return {
        user: {
            email: "dummy@dummy.com",
            name: "dummy"
        }
    };
};