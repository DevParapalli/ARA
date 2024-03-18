import { redirect } from "@sveltejs/kit"

export async function load({locals: { supabase, getSession } }) {
    const session = await getSession();
    // if the user is not logged in redirect back to the home page
    if (!session) {
        redirect(303, '/');
    }

    const {data} = await supabase.from('notebooks').select('*')
    console.log(data[0].id)
    const {data: data2} = await supabase.from('cells').select('*').eq('notebook', data[0].id)
    return {
        notebooks: data ?? [],
        cells: data2 ?? []
    }
}