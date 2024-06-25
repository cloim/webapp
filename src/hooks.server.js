import { redirect } from '@sveltejs/kit';

export const handle = async ({ event, resolve }) => {
    if (event.url.pathname === "/signout") throw redirect(303, "/signin");

    return resolve(event);
}