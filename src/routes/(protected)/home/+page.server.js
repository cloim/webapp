import { PUBLIC_APP_URI } from '$env/static/public';

export const load = async ({ cookies }) => {
    const token = cookies.get("token");

    // const res_samples = await fetch(`${PUBLIC_APP_URI}/samples`, {
    //     method: "GET",
    //     headers: {
    //         "Authorization": `Bearer ${token}`
    //     }
    // });
    // const samples = await res_samples.json();

    const result = {
        status: 200,
        message: '',
        data: {
            samples: []
        }
    }

    // if (res_samples.status == 401) {
    //     result.status = 401;
    //     result.message = '세션이 올바르지 않거나 만료되었습니다';
    // } else if (res_samples.status !== 200) {
    //     result.status = res_samples.status;
    //     result.message = '응답이 올바르지 않습니다';
    // } else {
    //     result.data.samples = samples;
    // }

    return result;
}
