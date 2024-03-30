import { Tables } from '$lib/supabaseTypes.js';
import { fail, redirect, error } from '@sveltejs/kit';

export const actions = {
    create: async (event) => {
        const { request, locals, params} = event;
        const formData = await request.formData();

        const name = formData.get('name');

        const notes = formData.get('notes');


        if (typeof name !== 'string' || typeof notes !== 'string') {
            return fail(400, {
                error: 'Invalid Input',
                name: name,
                notes: notes,
                error_on: '',
                message: 'Human Error',
            });
        }

        if (!name) {
            return fail(400, {
                error: 'Invalid Input',
                name: name,
                notes: notes,
                error_on: 'name',
                message: 'Name is required',
            });
        }

        if (notes.length > 1024) {
            return fail(400, {
                error: 'Invalid Input',
                name: name,
                notes: notes,
                error_on: 'notes',
                message: 'Notes must be less than 1024 characters',
            });
        }

        if (name.length < 5) {
            return fail(400, {
                error: 'Invalid Input',
                name: name,
                notes: notes,
                error_on: 'name',
                message: 'Name must be at least 5 characters',
            });
        }

        if (name.length > 128) {
            return fail(400, {
                error: 'Invalid Input',
                name: name,
                notes: notes,
                error_on: 'name',
                message: 'Name must be less than 128 characters',
            });
        }

        // Save the notebook to the database
        await locals.supabase.from('notebooks').update({
            name,
            notes,
        })
        .eq('id', params.id)

        // console.log(JSON.stringify(notebook))

                
        redirect(307, `/notebook/${params.id}`);
    },
};

export async function load({ locals: { getSession, supabase }, params }) {
    const session = await getSession();
    // If the user is not logged in redirect back to the home page, for login
    if (!session) {
        redirect(303, '/');
    }

    const {data, error: DBError} = await supabase.from('notebooks').select('*').eq('id', params.id).single();

    if (DBError) {
        error(500, 'Database Error');
    }

    return {
        notebook: data
    }

}
