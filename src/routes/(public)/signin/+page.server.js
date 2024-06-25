export const load = async ({ cookies }) => {
    cookies.set("token", "", { path: "/" });
}
