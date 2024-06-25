import { Post } from "$lib/network.js";

export const load = async ({ cookies }) => {
    const token = cookies.get("token");
    // const res = await Post("get_my_services", {}, token);

    // let services = [];
    // if (res.status == 200) {
    //     services = await res.json();
    //     services = services.map((s) => {
    //         return {
    //             name: s.name,
    //             value: s.id
    //         }
    //     });
    // }

    return {
        services: null
    }
}
