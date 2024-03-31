import { Tables } from '$lib/supabaseTypes.js';
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
    create: async (event) => {
        const { request, locals } = event;
        const formData = await request.formData();

        const name = formData.get('name');

        const notes = formData.get('notes');

        const user_id = formData.get('user_id');

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
        const { data: notebook, error } = await locals.supabase
            .from('notebooks')
            .insert({
                name,
                notes,
                created_by: (await locals.getSession()).user.id,
            })
            .select()
            .single()
            .returns<Tables<'notebooks'>>();

        // console.log(JSON.stringify(notebook))

        if (error) {
            return fail(500, {
                error: 'Database Error',
                name: name,
                notes: notes,
                error_on: '',
                message: error.message,
            });
        }

        // create an initial cell in the notebook

        await locals.supabase.from('cells').insert({
            notebook: notebook.id,
            content: 'Try editing this cell...',
            type: 'markdown',
        });

        redirect(307, `/notebook/${notebook.id}`);
    },
};

export async function load({ locals: { getSession } }) {
    const session = await getSession();
    // If the user is not logged in redirect back to the home page, for login
    if (!session) {
        redirect(303, '/');
    }
}
