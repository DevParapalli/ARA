/* eslint-disable @typescript-eslint/no-unused-vars */

import type { Actions } from './$types';

export const actions: Actions = {
    default: async (event) => {
        const {
            request,
            url,
            locals: { supabase },
        } = event;
        const formData = await request.formData();
        const email = formData.get('email') as string;
        const password = formData.get('password') as string;
        ('...');
    },
};
