import type { PageLoad } from "./$types";

export const load: PageLoad = async ({parent, params}) => {

    const {supabase} = await parent();

    const {data, error} = await supabase.from('notebooks').select('*').eq('id', params.id).single();
    if (!error) {
        return {
            info: data
        }
    }
    return {
        info: {
            name: "Loading",
            notes: "Loading..."
        }
    }
};