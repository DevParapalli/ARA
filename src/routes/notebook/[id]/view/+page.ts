import type { PageLoad } from "./$types";

export const load: PageLoad = async ({parent, params}) => {

    const {supabase} = await parent();

    const {data, error} = await supabase.from('cells').select('*').eq('notebook', params.id).order('created_at', { ascending: true });
    const {data: data2, error: error2} = await supabase.from('notebooks').select('*').eq('id', params.id).single();
    if (!error || !error2) {
        return {
            cells: data,
            info: data2
        };
    }

    return {
        cells: [],
        info: {
            name: "loading",
            notes: "loading..."
        }
    };
};