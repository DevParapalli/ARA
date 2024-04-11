import type { PageLoad } from "./$types";

export const load: PageLoad = async ({parent, params}) => {

    const {supabase} = await parent();

    const {data, error} = await supabase.from('cells').select('*').eq('notebook', params.id).order('created_at', { ascending: true });
    
    if (!error) {
        return {
            cells: data
        };
    }

    return {
        cells: []
    };
};