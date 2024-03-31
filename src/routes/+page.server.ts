import { redirect } from '@sveltejs/kit';
import type { Tables } from '$lib/supabaseTypes.js';

export async function load({ locals: { getSession, supabase } }) {
    const session = await getSession();
    // if the user is not logged in redirect back to the home page
    if (!session) {
        redirect(303, '/auth/login?next=/');
    }

    const { data, error } = await supabase
        .from('notebooks')
        .select('*')
        .eq('created_by', session.user.id)
        .returns<Tables<'notebooks'>[]>();

    if (error) {
        console.error(error);
        return {
            status: 500,
            error: 'Server Error',
        };
    }

    return {
        data,
    };
}
