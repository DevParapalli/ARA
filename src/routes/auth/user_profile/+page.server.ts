import type { Tables } from '$lib/supabaseTypes.js';
import { redirect } from '@sveltejs/kit';

export async function load({ locals: { supabase, getSession } }) {
    const session = await getSession();
    // if the user is not logged in redirect back to the home page
    if (!session) {
        redirect(303, '/');
    }

    const user = session.user;

    let userCustom: Tables<'users'>;

    const { data, error } = await supabase.from('users').select('*').eq('id', user.id).single();

    if (error) {
        console.error('Error fetching user data:', error);
    }

    if (!data) {
        console.error('No user data found for user:', user.id, 'creating new user record.');
        const { data: newUser, error } = await supabase.from('users').insert({ id: user.id }).single();
        if (error) {
            console.error('Error creating new user record:', error);
        } else {
            userCustom = newUser;
        }
    } else {
        userCustom = data;
    }

    return {
        user,
        user_data: userCustom,
    };
}
